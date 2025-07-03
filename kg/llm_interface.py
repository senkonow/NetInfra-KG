"""
LLM Interface for Knowledge Graph consumption
"""
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from .database import Neo4jKnowledgeGraph
from .models import EntityType


class KnowledgeGraphLLMInterface:
    """Interface for LLM consumption of the knowledge graph"""
    
    def __init__(self, kg: Neo4jKnowledgeGraph):
        self.kg = kg
    
    def get_topology_summary(self) -> Dict[str, Any]:
        """Get a high-level summary of the infrastructure topology"""
        stats = self.kg.get_statistics()
        
        summary = {
            "infrastructure_overview": {
                "total_entities": stats['total_entities'],
                "total_relationships": stats['total_relationships'],
                "entity_breakdown": stats['entity_counts'],
                "relationship_breakdown": stats['relationship_counts']
            },
            "topology_layers": {
                "network_layer": {
                    "switches": stats['entity_counts'].get('NetworkSwitch', 0),
                    "ports": stats['entity_counts'].get('NetworkPort', 0),
                    "vlans": stats['entity_counts'].get('VLAN', 0)
                },
                "compute_layer": {
                    "servers": stats['entity_counts'].get('Server', 0),
                    "virtual_machines": stats['entity_counts'].get('VirtualMachine', 0)
                },
                "container_layer": {
                    "kubernetes_pods": stats['entity_counts'].get('KubernetesPod', 0),
                    "containers": stats['entity_counts'].get('Container', 0)
                }
            },
            "generated_at": datetime.now().isoformat()
        }
        
        return summary
    
    def get_entity_context(self, entity_id: str, depth: int = 2) -> Dict[str, Any]:
        """Get comprehensive context for a specific entity with its relationships"""
        entity = self.kg.get_entity(entity_id)
        if not entity:
            return {"error": f"Entity {entity_id} not found"}
        
        context = {
            "entity": entity,
            "direct_neighbors": self.kg.get_entity_neighbors(entity_id),
            "paths_to_other_layers": [],
            "metadata": {
                "depth": depth,
                "query_time": datetime.now().isoformat()
            }
        }
        
        # Find paths to entities in different layers
        entity_type = entity.get('type')
        target_types = [
            EntityType.NETWORK_SWITCH, EntityType.SERVER, 
            EntityType.VIRTUAL_MACHINE, EntityType.KUBERNETES_POD, 
            EntityType.CONTAINER
        ]
        
        for target_type in target_types:
            if target_type.value != entity_type:
                target_entities = self.kg.query_entities_by_type(target_type)
                if target_entities:
                    sample_target = target_entities[0]
                    path = self.kg.get_topology_path(entity_id, sample_target['id'])
                    if path:
                        context["paths_to_other_layers"].append({
                            "target_type": target_type.value,
                            "path": path
                        })
        
        return context
    
    def get_network_path_analysis(self, source_id: str, target_id: str) -> Dict[str, Any]:
        """Analyze the network path between two entities"""
        path = self.kg.get_topology_path(source_id, target_id)
        
        if not path:
            return {"error": f"No path found between {source_id} and {target_id}"}
        
        analysis = {
            "path_summary": {
                "source_id": source_id,
                "target_id": target_id,
                "hop_count": len(path.get('nodes', [])) - 1,
                "relationship_chain": path.get('relationships', [])
            },
            "path_details": path,
            "infrastructure_layers_traversed": [],
            "potential_issues": [],
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # Analyze layers traversed
        for node in path.get('nodes', []):
            layer = self._get_infrastructure_layer(node.get('type'))
            if layer and layer not in analysis['infrastructure_layers_traversed']:
                analysis['infrastructure_layers_traversed'].append(layer)
        
        # Identify potential issues
        if analysis['path_summary']['hop_count'] > 10:
            analysis['potential_issues'].append("High hop count - may indicate complex routing")
        
        return analysis
    
    def _get_infrastructure_layer(self, entity_type: str) -> str:
        """Map entity type to infrastructure layer"""
        layer_mapping = {
            'NetworkSwitch': 'Network Layer',
            'NetworkPort': 'Network Layer',
            'VLAN': 'Network Layer',
            'Server': 'Compute Layer',
            'VirtualMachine': 'Virtualization Layer',
            'KubernetesPod': 'Container Orchestration Layer',
            'Container': 'Application Layer'
        }
        return layer_mapping.get(entity_type, 'Unknown Layer')
    
    def get_container_to_network_mapping(self, container_id: str) -> Dict[str, Any]:
        """Trace a container back to its network infrastructure"""
        container = self.kg.get_entity(container_id)
        if not container or container.get('type') != 'Container':
            return {"error": f"Container {container_id} not found"}
        
        # Find the complete path from container to network switch
        all_switches = self.kg.query_entities_by_type(EntityType.NETWORK_SWITCH)
        if not all_switches:
            return {"error": "No network switches found in topology"}
        
        # Use the first switch as representative
        switch = all_switches[0]
        path = self.kg.get_topology_path(container_id, switch['id'])
        
        mapping = {
            "container": container,
            "network_path": path,
            "infrastructure_stack": self._build_infrastructure_stack(path),
            "network_details": self._extract_network_details(path),
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        return mapping
    
    def _build_infrastructure_stack(self, path: Dict[str, Any]) -> List[Dict[str, str]]:
        """Build a readable infrastructure stack from path"""
        stack = []
        for node in path.get('nodes', []):
            stack.append({
                "id": node.get('id'),
                "name": node.get('name'),
                "type": node.get('type'),
                "layer": self._get_infrastructure_layer(node.get('type'))
            })
        return stack
    
    def _extract_network_details(self, path: Dict[str, Any]) -> Dict[str, Any]:
        """Extract network-specific details from path"""
        details = {
            "vlans": [],
            "switches": [],
            "servers": [],
            "ip_addresses": []
        }
        
        for node in path.get('nodes', []):
            node_type = node.get('type')
            if node_type == 'VLAN':
                details['vlans'].append(node)
            elif node_type == 'NetworkSwitch':
                details['switches'].append(node)
            elif node_type == 'Server':
                details['servers'].append(node)
        
        return details
    
    def get_security_context(self, entity_id: str) -> Dict[str, Any]:
        """Get security-relevant context for an entity"""
        entity = self.kg.get_entity(entity_id)
        if not entity:
            return {"error": f"Entity {entity_id} not found"}
        
        # Get all connected VLANs and their security implications
        neighbors = self.kg.get_entity_neighbors(entity_id)
        vlans = [n for n in neighbors if n.get('type') == 'VLAN']
        
        security_context = {
            "entity": entity,
            "network_segments": vlans,
            "access_paths": [],
            "security_boundaries": [],
            "recommendations": [],
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # Analyze security boundaries
        for vlan in vlans:
            if 'DMZ' in vlan.get('name', ''):
                security_context['security_boundaries'].append({
                    "type": "DMZ",
                    "vlan": vlan,
                    "risk_level": "High"
                })
            elif 'Production' in vlan.get('name', ''):
                security_context['security_boundaries'].append({
                    "type": "Production",
                    "vlan": vlan,
                    "risk_level": "Medium"
                })
        
        # Generate recommendations
        if len(vlans) > 3:
            security_context['recommendations'].append(
                "Entity connected to multiple VLANs - review network segmentation"
            )
        
        return security_context
    
    def get_resource_utilization_context(self, entity_type: EntityType) -> Dict[str, Any]:
        """Get resource utilization context for entities of a specific type"""
        entities = self.kg.query_entities_by_type(entity_type)
        
        context = {
            "entity_type": entity_type.value,
            "total_entities": len(entities),
            "resource_summary": {},
            "distribution": {},
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        if entity_type == EntityType.SERVER:
            cpu_cores = [e.get('cpu_cores', 0) for e in entities if e.get('cpu_cores')]
            memory_gb = [e.get('memory_gb', 0) for e in entities if e.get('memory_gb')]
            
            context['resource_summary'] = {
                "total_cpu_cores": sum(cpu_cores),
                "total_memory_gb": sum(memory_gb),
                "average_cpu_per_server": sum(cpu_cores) / len(cpu_cores) if cpu_cores else 0,
                "average_memory_per_server": sum(memory_gb) / len(memory_gb) if memory_gb else 0
            }
        
        elif entity_type == EntityType.VIRTUAL_MACHINE:
            cpu_cores = [e.get('cpu_cores', 0) for e in entities if e.get('cpu_cores')]
            memory_gb = [e.get('memory_gb', 0) for e in entities if e.get('memory_gb')]
            
            context['resource_summary'] = {
                "total_vm_cpu_cores": sum(cpu_cores),
                "total_vm_memory_gb": sum(memory_gb),
                "average_cpu_per_vm": sum(cpu_cores) / len(cpu_cores) if cpu_cores else 0,
                "average_memory_per_vm": sum(memory_gb) / len(memory_gb) if memory_gb else 0
            }
        
        return context
    
    def query_natural_language(self, query: str) -> Dict[str, Any]:
        """Process natural language queries about the infrastructure"""
        query_lower = query.lower()
        
        # Simple keyword-based query processing
        if "container" in query_lower and "network" in query_lower:
            containers = self.kg.query_entities_by_type(EntityType.CONTAINER)
            if containers:
                sample_container = containers[0]
                return self.get_container_to_network_mapping(sample_container['id'])
        
        elif "security" in query_lower:
            servers = self.kg.query_entities_by_type(EntityType.SERVER)
            if servers:
                return self.get_security_context(servers[0]['id'])
        
        elif "resource" in query_lower or "utilization" in query_lower:
            if "server" in query_lower:
                return self.get_resource_utilization_context(EntityType.SERVER)
            elif "vm" in query_lower or "virtual" in query_lower:
                return self.get_resource_utilization_context(EntityType.VIRTUAL_MACHINE)
        
        elif "topology" in query_lower or "overview" in query_lower:
            return self.get_topology_summary()
        
        elif "search" in query_lower:
            # Extract search term (simple approach)
            search_terms = query_lower.replace("search", "").strip().split()
            if search_terms:
                results = self.kg.search_entities(search_terms[0])
                return {
                    "search_query": query,
                    "search_term": search_terms[0],
                    "results": results,
                    "result_count": len(results)
                }
        
        return {
            "query": query,
            "response": "I understand you're asking about the infrastructure. Here's the topology overview:",
            "data": self.get_topology_summary()
        }
    
    def export_for_llm_training(self, format_type: str = "json") -> str:
        """Export knowledge graph data in a format suitable for LLM training"""
        graph_data = self.kg.get_full_topology_graph()
        
        if format_type == "json":
            return json.dumps(graph_data, indent=2)
        
        elif format_type == "text":
            # Convert to human-readable text format
            text_output = []
            text_output.append("INFRASTRUCTURE KNOWLEDGE GRAPH")
            text_output.append("=" * 50)
            text_output.append(f"Generated: {graph_data['metadata']['generated_at']}")
            text_output.append(f"Total Entities: {graph_data['metadata']['total_entities']}")
            text_output.append(f"Total Relationships: {graph_data['metadata']['total_relationships']}")
            text_output.append("")
            
            # Group entities by type
            entities_by_type = {}
            for entity in graph_data['entities']:
                entity_type = entity.get('type', 'Unknown')
                if entity_type not in entities_by_type:
                    entities_by_type[entity_type] = []
                entities_by_type[entity_type].append(entity)
            
            # Output each entity type
            for entity_type, entities in entities_by_type.items():
                text_output.append(f"{entity_type.upper()} ENTITIES ({len(entities)})")
                text_output.append("-" * 30)
                for entity in entities[:5]:  # Limit to first 5 for brevity
                    text_output.append(f"  - {entity.get('name', 'N/A')} (ID: {entity.get('id', 'N/A')})")
                if len(entities) > 5:
                    text_output.append(f"  ... and {len(entities) - 5} more")
                text_output.append("")
            
            # Output relationships
            text_output.append("RELATIONSHIPS")
            text_output.append("-" * 30)
            relationship_types = {}
            for rel in graph_data['relationships']:
                rel_type = rel.get('type', 'Unknown')
                if rel_type not in relationship_types:
                    relationship_types[rel_type] = 0
                relationship_types[rel_type] += 1
            
            for rel_type, count in relationship_types.items():
                text_output.append(f"  - {rel_type}: {count} connections")
            
            return "\n".join(text_output)
        
        return json.dumps(graph_data, indent=2)
    
    def get_cypher_queries_for_llm(self) -> List[Dict[str, str]]:
        """Generate useful Cypher queries for LLM to understand the data model"""
        queries = [
            {
                "description": "Get all network switches and their properties",
                "cypher": "MATCH (s:NetworkSwitch) RETURN s LIMIT 10"
            },
            {
                "description": "Find containers and their hosting path to physical servers",
                "cypher": """
                MATCH path = (c:Container)-[*]->(s:Server)
                RETURN c.name as container, s.hostname as server, 
                       [node in nodes(path) | node.name] as path_names
                LIMIT 5
                """
            },
            {
                "description": "Get VLAN connectivity overview",
                "cypher": """
                MATCH (v:VLAN)-[r]-(e:Entity)
                RETURN v.name as vlan, v.vlan_id as vlan_id, 
                       count(e) as connected_entities,
                       collect(DISTINCT labels(e)[1]) as entity_types
                """
            },
            {
                "description": "Find the complete infrastructure stack for a container",
                "cypher": """
                MATCH (c:Container)
                OPTIONAL MATCH path = (c)-[*]->(s:Server)
                RETURN c.name as container, 
                       [node in nodes(path) | {name: node.name, type: labels(node)[1]}] as stack
                LIMIT 3
                """
            },
            {
                "description": "Get resource utilization summary by server",
                "cypher": """
                MATCH (s:Server)
                OPTIONAL MATCH (s)-[:HOSTS]->(vm:VirtualMachine)
                RETURN s.hostname as server, s.cpu_cores as server_cpu, s.memory_gb as server_memory,
                       count(vm) as vm_count, sum(vm.cpu_cores) as allocated_cpu, sum(vm.memory_gb) as allocated_memory
                """
            }
        ]
        
        return queries 