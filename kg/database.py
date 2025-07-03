"""
Neo4j Database connection and management
"""
import os
from typing import List, Dict, Any, Optional, Union
import json
from datetime import datetime

from neo4j import GraphDatabase, Driver, Session
from neo4j.exceptions import ServiceUnavailable, AuthError

from .models import (
    BaseEntity, NetworkSwitch, NetworkPort, VLAN, Server, 
    VirtualMachine, KubernetesPod, Container, Relationship,
    EntityType, RelationshipType
)


class Neo4jKnowledgeGraph:
    """Neo4j Knowledge Graph Manager"""
    
    def __init__(self, uri: str = None, username: str = None, password: str = None):
        """
        Initialize Neo4j connection
        
        Args:
            uri: Neo4j database URI (default: bolt://localhost:7687)
            username: Neo4j username (default: neo4j)
            password: Neo4j password (default: from environment)
        """
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = username or os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password")
        
        self.driver: Optional[Driver] = None
        self._connect()
    
    def _connect(self) -> None:
        """Establish connection to Neo4j database"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri, 
                auth=(self.username, self.password)
            )
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            print(f"✅ Connected to Neo4j at {self.uri}")
        except (ServiceUnavailable, AuthError) as e:
            print(f"❌ Failed to connect to Neo4j: {e}")
            raise
    
    def close(self) -> None:
        """Close the database connection"""
        if self.driver:
            self.driver.close()
            print("🔌 Disconnected from Neo4j")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def setup_constraints_and_indexes(self) -> None:
        """Create database constraints and indexes"""
        constraints = [
            "CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE",
            "CREATE CONSTRAINT switch_id IF NOT EXISTS FOR (s:NetworkSwitch) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT port_id IF NOT EXISTS FOR (p:NetworkPort) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT vlan_id IF NOT EXISTS FOR (v:VLAN) REQUIRE v.id IS UNIQUE",
            "CREATE CONSTRAINT server_id IF NOT EXISTS FOR (s:Server) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT vm_id IF NOT EXISTS FOR (vm:VirtualMachine) REQUIRE vm.id IS UNIQUE",
            "CREATE CONSTRAINT pod_id IF NOT EXISTS FOR (p:KubernetesPod) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT container_id IF NOT EXISTS FOR (c:Container) REQUIRE c.id IS UNIQUE",
        ]
        
        indexes = [
            "CREATE INDEX entity_name IF NOT EXISTS FOR (e:Entity) ON (e.name)",
            "CREATE INDEX entity_type IF NOT EXISTS FOR (e:Entity) ON (e.type)",
            "CREATE INDEX vlan_vlan_id IF NOT EXISTS FOR (v:VLAN) ON (v.vlan_id)",
            "CREATE INDEX server_hostname IF NOT EXISTS FOR (s:Server) ON (s.hostname)",
            "CREATE INDEX vm_hostname IF NOT EXISTS FOR (vm:VirtualMachine) ON (vm.hostname)",
            "CREATE INDEX pod_namespace IF NOT EXISTS FOR (p:KubernetesPod) ON (p.namespace)",
            "CREATE INDEX container_image IF NOT EXISTS FOR (c:Container) ON (c.image)",
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    print(f"⚠️  Constraint creation warning: {e}")
            
            for index in indexes:
                try:
                    session.run(index)
                except Exception as e:
                    print(f"⚠️  Index creation warning: {e}")
        
        print("✅ Database constraints and indexes created")
    
    def create_entity(self, entity: BaseEntity) -> bool:
        """Create an entity in the knowledge graph"""
        with self.driver.session() as session:
            # Convert entity to dict, handling datetime serialization
            entity_dict = entity.dict()
            entity_dict['created_at'] = entity_dict['created_at'].isoformat()
            entity_dict['updated_at'] = entity_dict['updated_at'].isoformat()
            
            # Remove any remaining dict fields that could cause issues
            # (the JSON serialization should have already handled these)
            for key in list(entity_dict.keys()):
                if isinstance(entity_dict[key], dict):
                    print(f"⚠️  Removing dict field {key} - should be serialized as JSON")
                    del entity_dict[key]
            
            # Create node with Entity label and specific type label
            labels = f"Entity:{entity.type.value}"
            
            query = f"""
            CREATE (e:{labels})
            SET e = $properties
            RETURN e
            """
            
            try:
                result = session.run(query, properties=entity_dict)
                record = result.single()
                if record:
                    print(f"✅ Created {entity.type.value}: {entity.name}")
                    return True
            except Exception as e:
                print(f"❌ Failed to create entity {entity.name}: {e}")
                print(f"   Entity properties: {entity_dict}")
                return False
        
        return False
    
    def create_relationship(self, relationship: Relationship) -> bool:
        """Create a relationship between two entities"""
        with self.driver.session() as session:
            rel_dict = relationship.dict()
            rel_dict['created_at'] = rel_dict['created_at'].isoformat()
            
            # Remove any dict fields that could cause issues
            for key in list(rel_dict.keys()):
                if isinstance(rel_dict[key], dict):
                    print(f"⚠️  Removing dict field {key} from relationship - should be serialized as JSON")
                    del rel_dict[key]
            
            # Use the relationship properties (excluding source/target IDs and type)
            rel_properties = {k: v for k, v in rel_dict.items() if k not in ['source_id', 'target_id', 'relationship_type']}
            
            query = f"""
            MATCH (source:Entity {{id: $source_id}})
            MATCH (target:Entity {{id: $target_id}})
            CREATE (source)-[r:{relationship.relationship_type}]->(target)
            SET r = $properties
            RETURN r
            """
            
            try:
                result = session.run(
                    query, 
                    source_id=relationship.source_id,
                    target_id=relationship.target_id,
                    properties=rel_properties
                )
                record = result.single()
                if record:
                    print(f"✅ Created relationship: {relationship.source_id} -[{relationship.relationship_type}]-> {relationship.target_id}")
                    return True
            except Exception as e:
                print(f"❌ Failed to create relationship: {e}")
                print(f"   Relationship properties: {rel_properties}")
                return False
        
        return False
    
    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve an entity by ID"""
        with self.driver.session() as session:
            query = "MATCH (e:Entity {id: $entity_id}) RETURN e"
            result = session.run(query, entity_id=entity_id)
            record = result.single()
            if record:
                return dict(record['e'])
            return None
    
    def get_topology_path(self, start_entity_id: str, end_entity_id: str) -> List[Dict[str, Any]]:
        """Get the path between two entities in the topology"""
        with self.driver.session() as session:
            query = """
            MATCH path = shortestPath((start:Entity {id: $start_id})-[*]-(end:Entity {id: $end_id}))
            RETURN [node in nodes(path) | {id: node.id, name: node.name, type: node.type}] as nodes,
                   [rel in relationships(path) | type(rel)] as relationships
            """
            result = session.run(query, start_id=start_entity_id, end_id=end_entity_id)
            record = result.single()
            if record:
                return {
                    'nodes': record['nodes'],
                    'relationships': record['relationships']
                }
            return {}
    
    def get_entity_neighbors(self, entity_id: str, relationship_types: List[str] = None) -> List[Dict[str, Any]]:
        """Get neighboring entities"""
        with self.driver.session() as session:
            if relationship_types:
                rel_filter = "|".join(relationship_types)
                query = f"""
                MATCH (e:Entity {{id: $entity_id}})-[r:{rel_filter}]-(neighbor:Entity)
                RETURN neighbor, type(r) as relationship_type
                """
            else:
                query = """
                MATCH (e:Entity {id: $entity_id})-[r]-(neighbor:Entity)
                RETURN neighbor, type(r) as relationship_type
                """
            
            result = session.run(query, entity_id=entity_id)
            neighbors = []
            for record in result:
                neighbor_data = dict(record['neighbor'])
                neighbor_data['relationship_type'] = record['relationship_type']
                neighbors.append(neighbor_data)
            return neighbors
    
    def query_entities_by_type(self, entity_type: EntityType) -> List[Dict[str, Any]]:
        """Query all entities of a specific type"""
        with self.driver.session() as session:
            query = f"MATCH (e:{entity_type.value}) RETURN e"
            result = session.run(query)
            return [dict(record['e']) for record in result]
    
    def get_full_topology_graph(self) -> Dict[str, Any]:
        """Get the complete topology graph for LLM consumption"""
        with self.driver.session() as session:
            query = """
            MATCH (e:Entity)
            OPTIONAL MATCH (e)-[r]->(target:Entity)
            RETURN e as entity, 
                   collect({
                       target: target, 
                       relationship: type(r), 
                       properties: properties(r)
                   }) as relationships
            """
            result = session.run(query)
            
            graph = {
                'entities': [],
                'relationships': [],
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'total_entities': 0,
                    'total_relationships': 0
                }
            }
            
            for record in result:
                entity = dict(record['entity'])
                graph['entities'].append(entity)
                
                for rel in record['relationships']:
                    if rel['target']:  # Check if relationship exists
                        graph['relationships'].append({
                            'source': entity['id'],
                            'target': dict(rel['target'])['id'],
                            'type': rel['relationship'],
                            'properties': rel['properties']
                        })
            
            graph['metadata']['total_entities'] = len(graph['entities'])
            graph['metadata']['total_relationships'] = len(graph['relationships'])
            
            return graph
    
    def search_entities(self, search_term: str, entity_types: List[EntityType] = None) -> List[Dict[str, Any]]:
        """Search entities by name or properties"""
        with self.driver.session() as session:
            if entity_types:
                type_filter = "|".join([t.value for t in entity_types])
                query = f"""
                MATCH (e:{type_filter})
                WHERE e.name CONTAINS $search_term 
                   OR e.hostname CONTAINS $search_term
                   OR e.ip_address CONTAINS $search_term
                RETURN e
                ORDER BY e.name
                """
            else:
                query = """
                MATCH (e:Entity)
                WHERE e.name CONTAINS $search_term 
                   OR e.hostname CONTAINS $search_term
                   OR e.ip_address CONTAINS $search_term
                RETURN e
                ORDER BY e.name
                """
            
            result = session.run(query, search_term=search_term)
            return [dict(record['e']) for record in result]
    
    def clear_database(self) -> None:
        """Clear all data from the database (use with caution!)"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        print("🗑️  Database cleared")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        with self.driver.session() as session:
            stats_query = """
            MATCH (e:Entity)
            RETURN e.type as entity_type, count(e) as count
            ORDER BY count DESC
            """
            result = session.run(stats_query)
            entity_counts = {record['entity_type']: record['count'] for record in result}
            
            rel_query = "MATCH ()-[r]->() RETURN type(r) as rel_type, count(r) as count"
            result = session.run(rel_query)
            relationship_counts = {record['rel_type']: record['count'] for record in result}
            
            return {
                'entity_counts': entity_counts,
                'relationship_counts': relationship_counts,
                'total_entities': sum(entity_counts.values()),
                'total_relationships': sum(relationship_counts.values())
            } 