#!/usr/bin/env python3
"""
Network Infrastructure Knowledge Graph - Main Demo Script
"""
import os
import json
from dotenv import load_dotenv

from kg.database import Neo4jKnowledgeGraph
from kg.data_generator import InfrastructureDataGenerator
from kg.llm_interface import KnowledgeGraphLLMInterface
from kg.models import EntityType


def main():
    """Main demonstration function"""
    print("🚀 Network Infrastructure Knowledge Graph Demo")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Knowledge Graph
    print("\n1. Connecting to Neo4j...")
    try:
        kg = Neo4jKnowledgeGraph()
        print("✅ Successfully connected to Neo4j")
    except Exception as e:
        print(f"❌ Failed to connect to Neo4j: {e}")
        print("\n💡 Make sure Neo4j is running and credentials are correct")
        print("   Default connection: bolt://localhost:7687")
        print("   Default username: neo4j")
        print("   Default password: password")
        return
    
    # Setup database schema
    print("\n2. Setting up database schema...")
    kg.setup_constraints_and_indexes()
    
    # Check if database already has data
    stats = kg.get_statistics()
    if stats['total_entities'] > 0:
        print(f"📊 Database already contains {stats['total_entities']} entities")
        print("   Skipping data generation...")
        generate_data = False
    else:
        generate_data = True
    
    # Generate sample data if needed
    if generate_data:
        print("\n3. Generating sample infrastructure data...")
        generator = InfrastructureDataGenerator(kg)
        generator.populate_database()
    
    # Initialize LLM Interface
    print("\n4. Initializing LLM Interface...")
    llm_interface = KnowledgeGraphLLMInterface(kg)
    
    # Demonstrate various queries
    print("\n5. Demonstrating Knowledge Graph Queries...")
    print("=" * 50)
    
    # Get topology summary
    print("\n📊 TOPOLOGY SUMMARY")
    print("-" * 30)
    summary = llm_interface.get_topology_summary()
    print(f"Total Entities: {summary['infrastructure_overview']['total_entities']}")
    print(f"Total Relationships: {summary['infrastructure_overview']['total_relationships']}")
    print("\nEntity Breakdown:")
    for entity_type, count in summary['infrastructure_overview']['entity_breakdown'].items():
        print(f"  - {entity_type}: {count}")
    
    # Demonstrate container to network mapping
    print("\n🐳 CONTAINER TO NETWORK MAPPING")
    print("-" * 35)
    containers = kg.query_entities_by_type(EntityType.CONTAINER)
    if containers:
        sample_container = containers[0]
        print(f"Analyzing container: {sample_container['name']}")
        mapping = llm_interface.get_container_to_network_mapping(sample_container['id'])
        if 'infrastructure_stack' in mapping:
            print("\nInfrastructure Stack:")
            for i, layer in enumerate(mapping['infrastructure_stack']):
                print(f"  {i+1}. {layer['name']} ({layer['type']}) - {layer['layer']}")
    
    # Demonstrate resource utilization
    print("\n💾 RESOURCE UTILIZATION")
    print("-" * 25)
    server_resources = llm_interface.get_resource_utilization_context(EntityType.SERVER)
    if 'resource_summary' in server_resources:
        print("Server Resources:")
        summary = server_resources['resource_summary']
        print(f"  Total CPU Cores: {summary.get('total_cpu_cores', 0)}")
        print(f"  Total Memory (GB): {summary.get('total_memory_gb', 0)}")
        print(f"  Avg CPU per Server: {summary.get('average_cpu_per_server', 0):.1f}")
        print(f"  Avg Memory per Server: {summary.get('average_memory_per_server', 0):.1f} GB")
    
    vm_resources = llm_interface.get_resource_utilization_context(EntityType.VIRTUAL_MACHINE)
    if 'resource_summary' in vm_resources:
        print("\nVirtual Machine Resources:")
        summary = vm_resources['resource_summary']
        print(f"  Total VM CPU Cores: {summary.get('total_vm_cpu_cores', 0)}")
        print(f"  Total VM Memory (GB): {summary.get('total_vm_memory_gb', 0)}")
        print(f"  Avg CPU per VM: {summary.get('average_cpu_per_vm', 0):.1f}")
        print(f"  Avg Memory per VM: {summary.get('average_memory_per_vm', 0):.1f} GB")
    
    # Demonstrate natural language queries
    print("\n🗣️  NATURAL LANGUAGE QUERIES")
    print("-" * 32)
    queries = [
        "What is the topology overview?",
        "Show me container to network mapping",
        "What are the server resources?",
        "Search for production"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        response = llm_interface.query_natural_language(query)
        if 'data' in response and 'infrastructure_overview' in response['data']:
            overview = response['data']['infrastructure_overview']
            print(f"Response: Found {overview['total_entities']} entities with {overview['total_relationships']} relationships")
        elif 'result_count' in response:
            print(f"Response: Found {response['result_count']} matching entities")
        elif 'infrastructure_stack' in response:
            print(f"Response: Infrastructure stack with {len(response['infrastructure_stack'])} layers")
        else:
            print("Response: Query processed successfully")
    
    # Show useful Cypher queries
    print("\n📝 USEFUL CYPHER QUERIES FOR LLM")
    print("-" * 36)
    cypher_queries = llm_interface.get_cypher_queries_for_llm()
    for i, query_info in enumerate(cypher_queries[:3], 1):  # Show first 3
        print(f"\n{i}. {query_info['description']}")
        print(f"   Cypher: {query_info['cypher'].strip()}")
    
    # Export data for LLM training
    print("\n📤 EXPORTING DATA FOR LLM TRAINING")
    print("-" * 37)
    
    # Export as JSON
    json_export = llm_interface.export_for_llm_training("json")
    with open("infrastructure_kg_export.json", "w") as f:
        f.write(json_export)
    print("✅ Exported JSON format to: infrastructure_kg_export.json")
    
    # Export as text
    text_export = llm_interface.export_for_llm_training("text")
    with open("infrastructure_kg_export.txt", "w") as f:
        f.write(text_export)
    print("✅ Exported text format to: infrastructure_kg_export.txt")
    
    # Show sample of text export
    print("\nSample of text export:")
    print("-" * 25)
    lines = text_export.split('\n')[:15]  # First 15 lines
    for line in lines:
        print(line)
    print("...")
    
    print("\n🎉 Demo completed successfully!")
    print("\n💡 Next steps:")
    print("   1. Start Neo4j Browser at http://localhost:7474")
    print("   2. Explore the graph visually")
    print("   3. Try the exported Cypher queries")
    print("   4. Use the JSON/text exports for LLM training")
    print("   5. Extend the data model for your specific use case")
    
    # Close connection
    kg.close()


if __name__ == "__main__":
    main() 