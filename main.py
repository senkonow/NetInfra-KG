#!/usr/bin/env python3
# =============================================================================
# MAIN.PY - MAIN DEMONSTRATION SCRIPT FOR NETWORK INFRASTRUCTURE KNOWLEDGE GRAPH
# =============================================================================
# This is the "main" script that demonstrates our entire knowledge graph system
# Think of it like a "guided tour" that shows all the features of our software
#
# WHAT IS A MAIN SCRIPT?
# A main script is the entry point for a program - it's what you run to start everything
# It's like the "front door" of our software that leads you through all the rooms
# When someone wants to see what our knowledge graph can do, they run this script
#
# WHAT DOES THIS SCRIPT DO?
# 1. Connects to the Neo4j database
# 2. Sets up the database structure (constraints and indexes)
# 3. Generates sample network infrastructure data (if needed)
# 4. Demonstrates various ways to query and analyze the data
# 5. Shows how the system can be used with LLMs (Large Language Models)
# 6. Exports data for training AI models
#
# HOW TO RUN THIS SCRIPT:
# python main.py
# or
# python3 main.py

# SHEBANG LINE EXPLANATION
# The first line #!/usr/bin/env python3 is called a "shebang"
# It tells the operating system which program to use to run this script
# It's like telling your computer "use Python 3 to run this file"

# DOCSTRING - Documentation that explains what this script does
# =============================================================================
"""
Network Infrastructure Knowledge Graph - Main Demo Script

This script provides a comprehensive demonstration of the network infrastructure
knowledge graph system. It showcases:

1. Database connection and setup
2. Sample data generation
3. Various query capabilities
4. LLM (Large Language Model) integration
5. Data export for AI training
6. Real-world use cases and examples

The script is designed to be run standalone and provides a complete overview
of the system's capabilities for network administrators, developers, and
anyone interested in understanding how the knowledge graph works.
"""

# IMPORT STATEMENTS - Getting tools we need from other Python libraries
# =============================================================================

# os: For interacting with the operating system (file paths, environment variables)
import os

# json: For working with JSON data (JavaScript Object Notation)
# JSON is a way to store and exchange data that's easy for both humans and computers to read
import json

# dotenv: For loading environment variables from .env files
# Environment variables are settings stored outside the code for security and flexibility
from dotenv import load_dotenv

# Import our custom modules that we built for this knowledge graph system
# These are the "tools" we created to work with network infrastructure data

# Neo4jKnowledgeGraph: Our database manager class
from kg.database import Neo4jKnowledgeGraph

# InfrastructureDataGenerator: Creates sample network data for testing
from kg.data_generator import InfrastructureDataGenerator

# KnowledgeGraphLLMInterface: Provides natural language query capabilities
from kg.llm_interface import KnowledgeGraphLLMInterface

# EntityType: Enumeration of all the types of network entities we can store
from kg.models import EntityType


# MAIN FUNCTION - The heart of our demonstration
# =============================================================================

def main():
    """
    Main demonstration function
    
    WHAT IS A FUNCTION?
    A function is like a "recipe" - a set of instructions that does a specific task
    The main() function is special because it's the "master recipe" that coordinates
    all the other functions to create our complete demonstration
    
    WHAT DOES THIS FUNCTION DO?
    This function orchestrates the entire demonstration by:
    1. Setting up the database connection
    2. Creating sample data if needed
    3. Running various queries to show the system's capabilities
    4. Exporting data for use with AI/LLM systems
    """
    
    # DEMONSTRATION HEADER - Welcome message and introduction
    # -------------------------------------------------------------------------
    print("🚀 Network Infrastructure Knowledge Graph Demo")
    print("=" * 60)  # Print a line of 60 equal signs for visual separation
    
    # STEP 1: LOAD ENVIRONMENT VARIABLES
    # -------------------------------------------------------------------------
    # Environment variables are settings stored outside the code
    # They contain things like database passwords and configuration settings
    # load_dotenv() looks for a .env file and loads settings from it
    load_dotenv()
    
    # STEP 2: CONNECT TO NEO4J DATABASE
    # -------------------------------------------------------------------------
    print("\n1. Connecting to Neo4j...")  # \n creates a new line
    
    try:
        # WHAT IS TRY/EXCEPT?
        # try/except is like having a "backup plan" - we try to do something,
        # and if it fails, we have a plan for handling the error
        
        # Attempt to create a connection to the Neo4j database
        kg = Neo4jKnowledgeGraph()
        print("✅ Successfully connected to Neo4j")
        
    except Exception as e:
        # If connection fails, this code runs
        # Exception is a general term for "something went wrong"
        
        print(f"❌ Failed to connect to Neo4j: {e}")
        print("\n💡 Make sure Neo4j is running and credentials are correct")
        print("   Default connection: bolt://localhost:7687")
        print("   Default username: neo4j")
        print("   Default password: password")
        
        # return means "stop here and exit the function"
        # If we can't connect to the database, there's no point continuing
        return
    
    # STEP 3: SET UP DATABASE STRUCTURE
    # -------------------------------------------------------------------------
    print("\n2. Setting up database schema...")
    
    # Create constraints and indexes to ensure data quality and performance
    # Think of this like setting up the "rules" for our database
    kg.setup_constraints_and_indexes()
    
    # STEP 4: CHECK IF DATA ALREADY EXISTS
    # -------------------------------------------------------------------------
    # Before generating new data, check if the database already has data
    # This prevents creating duplicate data every time we run the script
    
    stats = kg.get_statistics()  # Get information about what's in the database
    
    if stats['total_entities'] > 0:
        # If the database already has entities, don't generate new ones
        print(f"📊 Database already contains {stats['total_entities']} entities")
        print("   Skipping data generation...")
        generate_data = False
    else:
        # If the database is empty, we'll generate sample data
        generate_data = True
    
    # STEP 5: GENERATE SAMPLE DATA (IF NEEDED)
    # -------------------------------------------------------------------------
    if generate_data:
        print("\n3. Generating sample infrastructure data...")
        
        # Create an instance of our data generator
        generator = InfrastructureDataGenerator(kg)
        
        # Generate and populate the database with sample network infrastructure
        # This creates switches, servers, VMs, containers, and their relationships
        generator.populate_database()
    
    # STEP 6: INITIALIZE LLM INTERFACE
    # -------------------------------------------------------------------------
    print("\n4. Initializing LLM Interface...")
    
    # Create an interface that allows natural language queries
    # This lets users ask questions in plain English about the network
    llm_interface = KnowledgeGraphLLMInterface(kg)
    
    # STEP 7: DEMONSTRATE VARIOUS QUERY CAPABILITIES
    # -------------------------------------------------------------------------
    print("\n5. Demonstrating Knowledge Graph Queries...")
    print("=" * 50)
    
    # DEMONSTRATION 1: TOPOLOGY SUMMARY
    # Show overall statistics about the network infrastructure
    print("\n📊 TOPOLOGY SUMMARY")
    print("-" * 30)  # Print a line of 30 dashes for visual separation
    
    # Get a high-level summary of all entities and relationships
    summary = llm_interface.get_topology_summary()
    
    # Display the summary information
    overview = summary['infrastructure_overview']
    print(f"Total Entities: {overview['total_entities']}")
    print(f"Total Relationships: {overview['total_relationships']}")
    print("\nEntity Breakdown:")
    
    # Loop through each entity type and show how many we have
    for entity_type, count in overview['entity_breakdown'].items():
        print(f"  - {entity_type}: {count}")
    
    # DEMONSTRATION 2: CONTAINER TO NETWORK MAPPING
    # Show how containers connect to the physical network infrastructure
    print("\n🐳 CONTAINER TO NETWORK MAPPING")
    print("-" * 35)
    
    # Get all containers from the database
    containers = kg.query_entities_by_type(EntityType.CONTAINER)
    
    if containers:  # If we have any containers
        # Pick the first container as an example
        sample_container = containers[0]
        print(f"Analyzing container: {sample_container['name']}")
        
        # Trace the path from container to network infrastructure
        mapping = llm_interface.get_container_to_network_mapping(sample_container['id'])
        
        if 'infrastructure_stack' in mapping:
            print("\nInfrastructure Stack:")
            # Show each layer of the infrastructure stack
            for i, layer in enumerate(mapping['infrastructure_stack']):
                # enumerate() gives us both the index (i) and the item (layer)
                print(f"  {i+1}. {layer['name']} ({layer['type']}) - {layer['layer']}")
    
    # DEMONSTRATION 3: RESOURCE UTILIZATION
    # Show how computing resources are allocated across the infrastructure
    print("\n💾 RESOURCE UTILIZATION")
    print("-" * 25)
    
    # Analyze server resources
    server_resources = llm_interface.get_resource_utilization_context(EntityType.SERVER)
    
    if 'resource_summary' in server_resources:
        print("Server Resources:")
        summary = server_resources['resource_summary']
        
        # Display server resource statistics
        # .get() safely gets a value from a dictionary, returning 0 if the key doesn't exist
        print(f"  Total CPU Cores: {summary.get('total_cpu_cores', 0)}")
        print(f"  Total Memory (GB): {summary.get('total_memory_gb', 0)}")
        print(f"  Avg CPU per Server: {summary.get('average_cpu_per_server', 0):.1f}")
        print(f"  Avg Memory per Server: {summary.get('average_memory_per_server', 0):.1f} GB")
    
    # Analyze virtual machine resources
    vm_resources = llm_interface.get_resource_utilization_context(EntityType.VIRTUAL_MACHINE)
    
    if 'resource_summary' in vm_resources:
        print("\nVirtual Machine Resources:")
        summary = vm_resources['resource_summary']
        
        # Display VM resource statistics
        print(f"  Total VM CPU Cores: {summary.get('total_vm_cpu_cores', 0)}")
        print(f"  Total VM Memory (GB): {summary.get('total_vm_memory_gb', 0)}")
        print(f"  Avg CPU per VM: {summary.get('average_cpu_per_vm', 0):.1f}")
        print(f"  Avg Memory per VM: {summary.get('average_memory_per_vm', 0):.1f} GB")
    
    # DEMONSTRATION 4: NATURAL LANGUAGE QUERIES
    # Show how users can ask questions in plain English
    print("\n🗣️  NATURAL LANGUAGE QUERIES")
    print("-" * 32)
    
    # Define a list of example queries that users might ask
    queries = [
        "What is the topology overview?",         # General overview question
        "Show me container to network mapping",   # Specific mapping question
        "What are the server resources?",         # Resource inquiry
        "Search for production"                   # Search query
    ]
    
    # Process each query and show the results
    for query in queries:
        print(f"\nQuery: '{query}'")
        
        # Send the natural language query to our LLM interface
        response = llm_interface.query_natural_language(query)
        
        # Analyze the response and provide a user-friendly summary
        # Different queries return different types of data, so we check what we got
        
        if 'data' in response and 'infrastructure_overview' in response['data']:
            # This is a topology overview response
            overview = response['data']['infrastructure_overview']
            print(f"Response: Found {overview['total_entities']} entities with {overview['total_relationships']} relationships")
            
        elif 'result_count' in response:
            # This is a search result response
            print(f"Response: Found {response['result_count']} matching entities")
            
        elif 'infrastructure_stack' in response:
            # This is an infrastructure mapping response
            print(f"Response: Infrastructure stack with {len(response['infrastructure_stack'])} layers")
            
        else:
            # Generic success message for other types of responses
            print("Response: Query processed successfully")
    
    # DEMONSTRATION 5: USEFUL CYPHER QUERIES
    # Show database queries that can be used for advanced analysis
    print("\n📝 USEFUL CYPHER QUERIES FOR LLM")
    print("-" * 36)
    
    # Get a list of pre-written database queries that are useful for analysis
    cypher_queries = llm_interface.get_cypher_queries_for_llm()
    
    # Show the first 3 queries as examples
    for i, query_info in enumerate(cypher_queries[:3], 1):  # [:3] takes first 3 items
        print(f"\n{i}. {query_info['description']}")
        print(f"   Cypher: {query_info['cypher'].strip()}")  # .strip() removes extra whitespace
    
    # STEP 8: EXPORT DATA FOR AI/LLM TRAINING
    # -------------------------------------------------------------------------
    print("\n📤 EXPORTING DATA FOR LLM TRAINING")
    print("-" * 37)
    
    # Export the knowledge graph data in formats that AI systems can use for training
    
    # Export as JSON format
    # JSON is a structured format that's easy for computers to read
    json_export = llm_interface.export_for_llm_training("json")
    
    # Write the JSON data to a file
    # "w" means "write mode" - create a new file or overwrite existing one
    with open("infrastructure_kg_export.json", "w") as f:
        f.write(json_export)
    print("✅ Exported JSON format to: infrastructure_kg_export.json")
    
    # Export as text format
    # Text format is human-readable and good for training language models
    text_export = llm_interface.export_for_llm_training("text")
    
    # Write the text data to a file
    with open("infrastructure_kg_export.txt", "w") as f:
        f.write(text_export)
    print("✅ Exported text format to: infrastructure_kg_export.txt")
    
    # Show a sample of the text export so users can see what it looks like
    print("\nSample of text export:")
    print("-" * 25)
    
    # Split the text into lines and show the first 15 lines
    lines = text_export.split('\n')[:15]  # split('\n') breaks text at newlines
    for line in lines:
        print(line)
    print("...")  # Indicate there's more content
    
    # DEMONSTRATION CONCLUSION
    # -------------------------------------------------------------------------
    print("\n🎉 Demo completed successfully!")
    
    # Provide helpful next steps for users
    print("\n💡 Next steps:")
    print("   1. Start Neo4j Browser at http://localhost:7474")
    print("   2. Explore the graph visually")
    print("   3. Try the exported Cypher queries")
    print("   4. Use the JSON/text exports for LLM training")
    print("   5. Extend the data model for your specific use case")
    
    # CLEANUP - Close database connection
    # -------------------------------------------------------------------------
    # Always close database connections when done to free up resources
    kg.close()


# SCRIPT EXECUTION CHECK
# =============================================================================
# This is a Python idiom that means "only run main() if this script is executed directly"
# It prevents the main() function from running if this file is imported by another script

if __name__ == "__main__":
    # WHAT DOES THIS MEAN?
    # __name__ is a special Python variable
    # When you run a script directly (python main.py), __name__ equals "__main__"
    # When you import a script from another file, __name__ equals the filename
    # 
    # This pattern lets us:
    # 1. Run the script directly: python main.py (calls main())
    # 2. Import functions from this script: from main import some_function (doesn't call main())
    
    main()  # Call the main function to start the demonstration 