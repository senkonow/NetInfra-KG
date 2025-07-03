# =============================================================================
# DATABASE.PY - NEO4J DATABASE CONNECTION AND MANAGEMENT
# =============================================================================
# This file handles all interactions with the Neo4j graph database
# Think of it as the "database manager" that knows how to:
# - Connect to the Neo4j database
# - Store entities (switches, servers, VMs, etc.) in the database
# - Create relationships between entities
# - Query the database to find information
# - Handle errors when things go wrong
#
# WHAT IS A GRAPH DATABASE?
# A graph database stores information as nodes (entities) and relationships (connections)
# Think of it like a social network:
# - Nodes are people (or in our case, network equipment)
# - Relationships are friendships (or in our case, connections like "HOSTS" or "RUNS_ON")
# - You can ask questions like "Who are John's friends?" or "What servers host this VM?"
#
# WHAT IS NEO4J?
# Neo4j is a popular graph database that stores nodes and relationships
# It uses a query language called Cypher (like SQL for graph databases)
# It's particularly good at finding paths and connections between entities

# DOCSTRING - Documentation that explains what this file does
# =============================================================================
"""
Neo4j Database connection and management

This file provides the KnowledgeGraphDB class which handles all interactions
with the Neo4j graph database. It includes:

- Database connection management (connecting, disconnecting, error handling)
- Entity creation and storage (switches, servers, VMs, containers, etc.)
- Relationship creation (connections between entities)
- Query operations (finding entities, getting topology paths)
- Database maintenance (constraints, indexes, statistics)
- Error handling and logging

The class abstracts away the complexity of Neo4j operations and provides
a simple interface for storing and retrieving network topology information.
"""

# IMPORT STATEMENTS - Getting tools we need from other Python libraries
# =============================================================================

# os: For reading environment variables (like database passwords)
import os

# typing: For specifying what types of data our functions expect
# This helps catch errors and makes code more readable
from typing import List, Dict, Any, Optional, Union

# json: For converting between Python objects and JSON strings
# We use this when working with complex data stored as JSON
import json

# datetime: For working with dates and times
# We track when entities and relationships were created
from datetime import datetime

# neo4j: The official Python library for connecting to Neo4j database
# GraphDatabase: Main class for creating database connections
# Driver: Represents a connection to the database
# Session: Represents a database session for running queries
from neo4j import GraphDatabase, Driver, Session

# neo4j.exceptions: Error types that can occur when using Neo4j
# ServiceUnavailable: Database is not running or unreachable
# AuthError: Username/password authentication failed
from neo4j.exceptions import ServiceUnavailable, AuthError

# Import our data models from the models.py file
# These are the classes that define our entity types and relationships
from .models import (
    BaseEntity, NetworkSwitch, NetworkPort, VLAN, Server, 
    VirtualMachine, KubernetesPod, Container, Relationship,
    EntityType, RelationshipType
)


# NEO4J KNOWLEDGE GRAPH CLASS - Main database management class
# =============================================================================

class Neo4jKnowledgeGraph:
    """
    Neo4j Knowledge Graph Manager
    
    WHAT IS THIS CLASS?
    This class is like a "database manager" that handles all operations
    with the Neo4j graph database. It's responsible for:
    
    1. Connecting to the database
    2. Creating entities (network equipment)
    3. Creating relationships (connections between equipment)
    4. Querying the database for information
    5. Handling errors and maintaining the database
    
    OBJECT-ORIENTED PROGRAMMING CONCEPT:
    This class is like a "blueprint" for creating database managers
    Each instance of this class represents one connection to a Neo4j database
    """
    
    def __init__(self, uri: str = None, username: str = None, password: str = None):
        """
        Initialize Neo4j connection
        
        WHAT IS __init__?
        __init__ is a special method called a "constructor"
        It's automatically called when you create a new instance of this class
        Think of it like the "setup instructions" for a new database manager
        
        PARAMETERS:
        uri: str = None means:
        - uri is the database address (like a web URL)
        - str means it should be a string
        - = None means if no uri is provided, use None as default
        
        EXAMPLE USAGE:
        # Create a database manager with default settings
        db = Neo4jKnowledgeGraph()
        
        # Create a database manager with custom settings
        db = Neo4jKnowledgeGraph(
            uri="bolt://my-server:7687",
            username="admin",
            password="mypassword"
        )
        """
        # Set up database connection parameters
        # If no uri is provided, try to get it from environment variables
        # If that fails too, use the default local database address
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        
        # Same logic for username - try parameter, then environment, then default
        self.username = username or os.getenv("NEO4J_USERNAME", "neo4j")
        
        # Same logic for password - try parameter, then environment, then default
        self.password = password or os.getenv("NEO4J_PASSWORD", "password")
        
        # Initialize driver to None (we'll create it in _connect method)
        # Optional[Driver] means this can be a Driver object or None
        self.driver: Optional[Driver] = None
        
        # Attempt to connect to the database
        self._connect()
    
    def _connect(self) -> None:
        """
        Establish connection to Neo4j database
        
        WHAT IS A PRIVATE METHOD?
        Methods starting with underscore (_) are "private" methods
        They're meant to be used only inside the class, not by external code
        Think of them like "internal helper functions"
        
        WHY SEPARATE CONNECTION LOGIC?
        By putting connection logic in a separate method, we can:
        1. Keep the __init__ method clean and focused
        2. Reuse connection logic if we need to reconnect
        3. Handle connection errors in one place
        """
        try:
            # Create a driver (connection) to the Neo4j database
            # GraphDatabase.driver() is like opening a connection to the database
            # auth=(username, password) provides the login credentials
            self.driver = GraphDatabase.driver(
                self.uri, 
                auth=(self.username, self.password)
            )
            
            # Test the connection by running a simple query
            # This ensures the database is reachable and credentials are correct
            with self.driver.session() as session:
                # "RETURN 1" is like saying "hello" to the database
                # If it responds, we know the connection works
                session.run("RETURN 1")
            
            # If we get here, the connection was successful
            print(f"✅ Connected to Neo4j at {self.uri}")
            
        except (ServiceUnavailable, AuthError) as e:
            # EXCEPTION HANDLING - What to do when things go wrong
            # ServiceUnavailable: Database is not running or unreachable
            # AuthError: Username/password is incorrect
            
            print(f"❌ Failed to connect to Neo4j: {e}")
            
            # Re-raise the exception so the calling code knows there was an error
            # This is like saying "I can't handle this error, so I'm passing it up"
            raise
    
    def close(self) -> None:
        """
        Close the database connection
        
        WHY CLOSE CONNECTIONS?
        Database connections use system resources (memory, network sockets)
        It's good practice to close them when you're done to free up resources
        Think of it like closing a file after you're done reading it
        """
        if self.driver:  # Only close if we have a connection
            self.driver.close()
            print("🔌 Disconnected from Neo4j")
    
    def __enter__(self):
        """
        Context manager entry method
        
        WHAT IS A CONTEXT MANAGER?
        A context manager allows you to use the "with" statement
        It ensures cleanup happens even if an error occurs
        
        EXAMPLE:
        with Neo4jKnowledgeGraph() as db:
            # Do database operations here
            db.create_entity(some_entity)
        # Database connection is automatically closed when exiting the 'with' block
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit method
        
        This is automatically called when exiting a 'with' block
        It ensures the database connection is properly closed
        """
        self.close()
    
    def setup_constraints_and_indexes(self) -> None:
        """
        Create database constraints and indexes
        
        WHAT ARE CONSTRAINTS?
        Constraints are rules that ensure data quality
        For example, "every entity must have a unique ID"
        Think of them like "data quality rules"
        
        WHAT ARE INDEXES?
        Indexes speed up database queries
        They're like an "index" in a book that helps you find things faster
        For example, an index on "name" makes searching by name much faster
        
        WHY DO WE NEED THEM?
        1. Constraints prevent duplicate entities and ensure data integrity
        2. Indexes make queries much faster, especially with large datasets
        3. They help the database optimize query performance
        """
        
        # Define constraints - rules that ensure data quality
        constraints = [
            # Ensure every Entity has a unique ID
            "CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE",
            
            # Ensure every NetworkSwitch has a unique ID
            "CREATE CONSTRAINT switch_id IF NOT EXISTS FOR (s:NetworkSwitch) REQUIRE s.id IS UNIQUE",
            
            # Ensure every NetworkPort has a unique ID
            "CREATE CONSTRAINT port_id IF NOT EXISTS FOR (p:NetworkPort) REQUIRE p.id IS UNIQUE",
            
            # Ensure every VLAN has a unique ID
            "CREATE CONSTRAINT vlan_id IF NOT EXISTS FOR (v:VLAN) REQUIRE v.id IS UNIQUE",
            
            # Ensure every Server has a unique ID
            "CREATE CONSTRAINT server_id IF NOT EXISTS FOR (s:Server) REQUIRE s.id IS UNIQUE",
            
            # Ensure every VirtualMachine has a unique ID
            "CREATE CONSTRAINT vm_id IF NOT EXISTS FOR (vm:VirtualMachine) REQUIRE vm.id IS UNIQUE",
            
            # Ensure every KubernetesPod has a unique ID
            "CREATE CONSTRAINT pod_id IF NOT EXISTS FOR (p:KubernetesPod) REQUIRE p.id IS UNIQUE",
            
            # Ensure every Container has a unique ID
            "CREATE CONSTRAINT container_id IF NOT EXISTS FOR (c:Container) REQUIRE c.id IS UNIQUE",
        ]
        
        # Define indexes - speed up common queries
        indexes = [
            # Index on entity name for faster name-based searches
            "CREATE INDEX entity_name IF NOT EXISTS FOR (e:Entity) ON (e.name)",
            
            # Index on entity type for faster type-based searches
            "CREATE INDEX entity_type IF NOT EXISTS FOR (e:Entity) ON (e.type)",
            
            # Index on VLAN ID for faster VLAN searches
            "CREATE INDEX vlan_vlan_id IF NOT EXISTS FOR (v:VLAN) ON (v.vlan_id)",
            
            # Index on server hostname for faster server searches
            "CREATE INDEX server_hostname IF NOT EXISTS FOR (s:Server) ON (s.hostname)",
            
            # Index on VM hostname for faster VM searches
            "CREATE INDEX vm_hostname IF NOT EXISTS FOR (vm:VirtualMachine) ON (vm.hostname)",
            
            # Index on pod namespace for faster Kubernetes pod searches
            "CREATE INDEX pod_namespace IF NOT EXISTS FOR (p:KubernetesPod) ON (p.namespace)",
            
            # Index on container image for faster container searches
            "CREATE INDEX container_image IF NOT EXISTS FOR (c:Container) ON (c.image)",
        ]
        
        # Execute constraints and indexes
        with self.driver.session() as session:
            # Create constraints
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    # Warning instead of error because constraint might already exist
                    print(f"⚠️  Constraint creation warning: {e}")
            
            # Create indexes
            for index in indexes:
                try:
                    session.run(index)
                except Exception as e:
                    # Warning instead of error because index might already exist
                    print(f"⚠️  Index creation warning: {e}")
        
        print("✅ Database constraints and indexes created")
    
    def create_entity(self, entity: BaseEntity) -> bool:
        """
        Create an entity in the knowledge graph
        
        WHAT DOES THIS METHOD DO?
        This method takes an entity object (like a NetworkSwitch or Server)
        and stores it in the Neo4j database as a node
        
        PARAMETERS:
        entity: BaseEntity - Any entity that inherits from BaseEntity
        (NetworkSwitch, Server, VirtualMachine, etc.)
        
        RETURN VALUE:
        bool - True if successful, False if failed
        
        EXAMPLE USAGE:
        switch = NetworkSwitch(id="SW-001", name="Main Switch")
        success = db.create_entity(switch)
        if success:
            print("Switch created successfully!")
        """
        with self.driver.session() as session:
            # Convert entity object to dictionary
            # .dict() is a Pydantic method that converts the object to a dictionary
            entity_dict = entity.dict()
            
            # Handle datetime serialization
            # Neo4j doesn't understand Python datetime objects, so we convert them to strings
            # .isoformat() converts datetime to ISO format string (e.g., "2023-01-15T10:30:00")
            entity_dict['created_at'] = entity_dict['created_at'].isoformat()
            entity_dict['updated_at'] = entity_dict['updated_at'].isoformat()
            
            # Safety check: Remove any remaining dictionary fields
            # Neo4j can't store complex dictionaries, only primitive types
            # Our models should have already converted dicts to JSON strings,
            # but this is a safety check in case something was missed
            for key in list(entity_dict.keys()):
                if isinstance(entity_dict[key], dict):
                    print(f"⚠️  Removing dict field {key} - should be serialized as JSON")
                    del entity_dict[key]
            
            # Create the database query
            # In Neo4j, we create nodes with labels
            # Labels are like "categories" or "types" for nodes
            # We give each node two labels: "Entity" (common to all) and the specific type
            labels = f"Entity:{entity.type.value}"
            
            # Cypher query to create the node
            # CREATE creates a new node
            # SET assigns properties to the node
            # RETURN returns the created node (for confirmation)
            query = f"""
            CREATE (e:{labels})
            SET e = $properties
            RETURN e
            """
            
            try:
                # Execute the query
                # $properties is a parameter that gets replaced with entity_dict
                result = session.run(query, properties=entity_dict)
                
                # Check if the query was successful
                record = result.single()  # Get the first (and only) result
                if record:
                    print(f"✅ Created {entity.type.value}: {entity.name}")
                    return True
                    
            except Exception as e:
                # Error handling - print detailed error information
                print(f"❌ Failed to create entity {entity.name}: {e}")
                print(f"   Entity properties: {entity_dict}")
                return False
        
        return False
    
    def create_relationship(self, relationship: Relationship) -> bool:
        """
        Create a relationship between two entities
        
        WHAT DOES THIS METHOD DO?
        This method creates a connection (relationship) between two entities
        For example, it can create a "HOSTS" relationship between a Server and a VM
        
        PARAMETERS:
        relationship: Relationship - A relationship object defining the connection
        
        RETURN VALUE:
        bool - True if successful, False if failed
        
        EXAMPLE USAGE:
        rel = Relationship(
            source_id="server-001",
            target_id="vm-001", 
            relationship_type="HOSTS"
        )
        success = db.create_relationship(rel)
        """
        with self.driver.session() as session:
            # Convert relationship object to dictionary
            rel_dict = relationship.dict()
            
            # Handle datetime serialization
            rel_dict['created_at'] = rel_dict['created_at'].isoformat()
            
            # Safety check: Remove any dictionary fields
            for key in list(rel_dict.keys()):
                if isinstance(rel_dict[key], dict):
                    print(f"⚠️  Removing dict field {key} from relationship - should be serialized as JSON")
                    del rel_dict[key]
            
            # Prepare relationship properties
            # We don't include source_id, target_id, and relationship_type in the properties
            # because they're used to create the relationship structure, not as properties
            rel_properties = {k: v for k, v in rel_dict.items() 
                            if k not in ['source_id', 'target_id', 'relationship_type']}
            
            # Cypher query to create the relationship
            # MATCH finds the source and target nodes
            # CREATE creates the relationship between them
            # The relationship type is dynamic (e.g., HOSTS, RUNS_ON, CONTAINS)
            query = f"""
            MATCH (source:Entity {{id: $source_id}})
            MATCH (target:Entity {{id: $target_id}})
            CREATE (source)-[r:{relationship.relationship_type}]->(target)
            SET r = $properties
            RETURN r
            """
            
            try:
                # Execute the query with parameters
                result = session.run(
                    query, 
                    source_id=relationship.source_id,
                    target_id=relationship.target_id,
                    properties=rel_properties
                )
                
                # Check if the query was successful
                record = result.single()
                if record:
                    print(f"✅ Created relationship: {relationship.source_id} -[{relationship.relationship_type}]-> {relationship.target_id}")
                    return True
                    
            except Exception as e:
                # Error handling
                print(f"❌ Failed to create relationship: {e}")
                print(f"   Relationship properties: {rel_properties}")
                return False
        
        return False
    
    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an entity by ID
        
        WHAT DOES THIS METHOD DO?
        This method finds and returns an entity from the database using its ID
        
        PARAMETERS:
        entity_id: str - The unique ID of the entity to find
        
        RETURN VALUE:
        Optional[Dict[str, Any]] - The entity data as a dictionary, or None if not found
        
        EXAMPLE USAGE:
        entity = db.get_entity("server-001")
        if entity:
            print(f"Found entity: {entity['name']}")
        else:
            print("Entity not found")
        """
        with self.driver.session() as session:
            # Simple query to find an entity by ID
            query = "MATCH (e:Entity {id: $entity_id}) RETURN e"
            
            # Execute the query
            result = session.run(query, entity_id=entity_id)
            
            # Get the first result (should be only one due to unique constraint)
            record = result.single()
            
            if record:
                # Convert the Neo4j node to a Python dictionary
                return dict(record['e'])
            
            return None
    
    def get_topology_path(self, start_entity_id: str, end_entity_id: str) -> List[Dict[str, Any]]:
        """
        Get the path between two entities in the topology
        
        WHAT DOES THIS METHOD DO?
        This method finds the shortest path between two entities in the network topology
        For example, it can find the path from a Container to a NetworkSwitch
        
        PARAMETERS:
        start_entity_id: str - ID of the starting entity
        end_entity_id: str - ID of the ending entity
        
        RETURN VALUE:
        List[Dict[str, Any]] - Path information including nodes and relationships
        
        EXAMPLE USAGE:
        path = db.get_topology_path("container-001", "switch-001")
        if path:
            print(f"Path found with {len(path)} hops")
        """
        with self.driver.session() as session:
            # Cypher query to find the shortest path between two entities
            # shortestPath() is a Neo4j function that finds the shortest connection
            # [*] means "any number of relationships of any type"
            # nodes(path) extracts all nodes from the path
            # relationships(path) extracts all relationships from the path
            query = """
            MATCH path = shortestPath((start:Entity {id: $start_id})-[*]-(end:Entity {id: $end_id}))
            RETURN [node in nodes(path) | {id: node.id, name: node.name, type: node.type}] as nodes,
                   [rel in relationships(path) | type(rel)] as relationships
            """
            
            # Execute the query
            result = session.run(query, start_id=start_entity_id, end_id=end_entity_id)
            record = result.single()
            
            if record:
                return {
                    'nodes': record['nodes'],
                    'relationships': record['relationships']
                }
            
            return []
    
    def get_entity_neighbors(self, entity_id: str, relationship_types: List[str] = None) -> List[Dict[str, Any]]:
        """
        Get all entities directly connected to a given entity
        
        WHAT DOES THIS METHOD DO?
        This method finds all entities that are directly connected to a given entity
        For example, it can find all VMs hosted by a specific server
        
        PARAMETERS:
        entity_id: str - ID of the entity to find neighbors for
        relationship_types: List[str] - Optional list of relationship types to filter by
        
        RETURN VALUE:
        List[Dict[str, Any]] - List of neighboring entities
        
        EXAMPLE USAGE:
        neighbors = db.get_entity_neighbors("server-001", ["HOSTS"])
        for neighbor in neighbors:
            print(f"Server hosts: {neighbor['name']}")
        """
        with self.driver.session() as session:
            if relationship_types:
                # Build a filter for specific relationship types
                # | means "OR" in Cypher
                rel_filter = "|".join(relationship_types)
                query = f"""
                MATCH (e:Entity {{id: $entity_id}})-[r:{rel_filter}]-(neighbor:Entity)
                RETURN neighbor, type(r) as relationship_type
                """
            else:
                # Get all neighbors regardless of relationship type
                query = """
                MATCH (e:Entity {id: $entity_id})-[r]-(neighbor:Entity)
                RETURN neighbor, type(r) as relationship_type
                """
            
            # Execute the query
            result = session.run(query, entity_id=entity_id)
            
            # Convert results to list of dictionaries
            neighbors = []
            for record in result:
                neighbor_data = dict(record['neighbor'])
                neighbor_data['relationship_type'] = record['relationship_type']
                neighbors.append(neighbor_data)
            
            return neighbors
    
    def query_entities_by_type(self, entity_type: EntityType) -> List[Dict[str, Any]]:
        """
        Get all entities of a specific type
        
        WHAT DOES THIS METHOD DO?
        This method finds all entities of a specific type
        For example, it can find all NetworkSwitches or all Servers
        
        PARAMETERS:
        entity_type: EntityType - The type of entities to find
        
        RETURN VALUE:
        List[Dict[str, Any]] - List of entities of the specified type
        
        EXAMPLE USAGE:
        servers = db.query_entities_by_type(EntityType.SERVER)
        print(f"Found {len(servers)} servers")
        """
        with self.driver.session() as session:
            # Query for entities of a specific type
            query = f"MATCH (e:{entity_type.value}) RETURN e"
            result = session.run(query)
            
            # Convert results to list of dictionaries
            entities = []
            for record in result:
                entities.append(dict(record['e']))
            
            return entities
    
    def get_full_topology_graph(self) -> Dict[str, Any]:
        """
        Get the complete topology graph with all entities and relationships
        
        WHAT DOES THIS METHOD DO?
        This method retrieves the entire network topology from the database
        It returns all entities and all relationships between them
        
        RETURN VALUE:
        Dict[str, Any] - Complete graph data with nodes and relationships
        
        EXAMPLE USAGE:
        graph = db.get_full_topology_graph()
        print(f"Total entities: {len(graph['nodes'])}")
        print(f"Total relationships: {len(graph['relationships'])}")
        """
        with self.driver.session() as session:
            # Query to get all entities (nodes)
            nodes_query = "MATCH (e:Entity) RETURN e"
            nodes_result = session.run(nodes_query)
            
            # Convert nodes to list of dictionaries
            nodes = []
            for record in nodes_result:
                nodes.append(dict(record['e']))
            
            # Query to get all relationships
            relationships_query = """
            MATCH (source:Entity)-[r]->(target:Entity)
            RETURN source.id as source_id, target.id as target_id, 
                   type(r) as relationship_type, properties(r) as properties
            """
            relationships_result = session.run(relationships_query)
            
            # Convert relationships to list of dictionaries
            relationships = []
            for record in relationships_result:
                rel_data = {
                    'source_id': record['source_id'],
                    'target_id': record['target_id'],
                    'relationship_type': record['relationship_type'],
                    'properties': dict(record['properties'])
                }
                relationships.append(rel_data)
            
            return {
                'nodes': nodes,
                'relationships': relationships
            }
    
    def search_entities(self, search_term: str, entity_types: List[EntityType] = None) -> List[Dict[str, Any]]:
        """
        Search for entities by name or other properties
        
        WHAT DOES THIS METHOD DO?
        This method searches for entities that match a search term
        It can search by name, and optionally filter by entity type
        
        PARAMETERS:
        search_term: str - The term to search for
        entity_types: List[EntityType] - Optional list of entity types to search within
        
        RETURN VALUE:
        List[Dict[str, Any]] - List of entities matching the search criteria
        
        EXAMPLE USAGE:
        results = db.search_entities("web", [EntityType.SERVER, EntityType.VIRTUAL_MACHINE])
        for result in results:
            print(f"Found: {result['name']} ({result['type']})")
        """
        with self.driver.session() as session:
            if entity_types:
                # Build a filter for specific entity types
                type_filter = "|".join([et.value for et in entity_types])
                query = f"""
                MATCH (e:Entity)
                WHERE e.name CONTAINS $search_term 
                AND any(label in labels(e) WHERE label IN [{', '.join([f"'{et.value}'" for et in entity_types])}])
                RETURN e
                """
            else:
                # Search all entity types
                query = """
                MATCH (e:Entity)
                WHERE e.name CONTAINS $search_term
                RETURN e
                """
            
            # Execute the query
            result = session.run(query, search_term=search_term)
            
            # Convert results to list of dictionaries
            entities = []
            for record in result:
                entities.append(dict(record['e']))
            
            return entities
    
    def clear_database(self) -> None:
        """
        Clear all data from the database
        
        WARNING: This method deletes ALL data from the database!
        Use with extreme caution!
        
        WHAT DOES THIS METHOD DO?
        This method removes all entities and relationships from the database
        It's useful for testing or when you want to start fresh
        """
        with self.driver.session() as session:
            # Delete all relationships first (Neo4j requirement)
            session.run("MATCH ()-[r]->() DELETE r")
            
            # Then delete all nodes
            session.run("MATCH (n) DELETE n")
            
            print("🗑️  Database cleared")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics
        
        WHAT DOES THIS METHOD DO?
        This method returns statistics about the database contents
        It counts how many entities and relationships exist
        
        RETURN VALUE:
        Dict[str, Any] - Statistics about the database
        
        EXAMPLE USAGE:
        stats = db.get_statistics()
        print(f"Total entities: {stats['total_entities']}")
        print(f"Total relationships: {stats['total_relationships']}")
        """
        with self.driver.session() as session:
            # Count total entities
            total_entities_result = session.run("MATCH (e:Entity) RETURN count(e) as count")
            total_entities = total_entities_result.single()['count']
            
            # Count total relationships
            total_relationships_result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            total_relationships = total_relationships_result.single()['count']
            
            # Count entities by type
            entity_counts = {}
            for entity_type in EntityType:
                result = session.run(f"MATCH (e:{entity_type.value}) RETURN count(e) as count")
                entity_counts[entity_type.value] = result.single()['count']
            
            return {
                'total_entities': total_entities,
                'total_relationships': total_relationships,
                'entity_counts': entity_counts
            } 