# Network Infrastructure Knowledge Graph

A Neo4j-powered knowledge graph system designed to model and analyze network infrastructure topology for LLM consumption. This system represents the complete stack from network switches to containers, enabling AI systems to understand and reason about infrastructure relationships.

## 🏗️ Architecture Overview

The system models a hierarchical network infrastructure:

```
Network Switch → Network Port → VLAN → Server → Virtual Machine → Kubernetes Pod → Container
```

### Entity Types

- **NetworkSwitch**: Physical network switches with ports and management interfaces
- **NetworkPort**: Individual ports on network switches
- **VLAN**: Virtual LANs for network segmentation
- **Server**: Physical servers with hardware specifications
- **VirtualMachine**: Virtual machines running on physical servers
- **KubernetesPod**: Kubernetes pods for container orchestration
- **Container**: Application containers with runtime configurations

### Relationship Types

- `CONNECTED_TO`: Network connectivity relationships
- `HOSTS`: Server hosting virtual machines
- `RUNS_ON`: Pods running on virtual machines
- `BELONGS_TO`: Network membership relationships
- `CONTAINS`: Containment relationships (switch contains ports, pods contain containers)
- `DEPLOYED_ON`: Deployment relationships
- `PART_OF`: Hierarchical membership

## 🚀 Features

- **Complete Infrastructure Modeling**: Models the full stack from network to application layer
- **LLM-Ready Interface**: Provides structured data and natural language query interface
- **Path Analysis**: Traces connections between any two entities in the topology
- **Resource Utilization**: Analyzes compute resources across the infrastructure
- **Security Context**: Provides security-relevant information about network segments
- **Data Export**: Exports knowledge graph data for LLM training in JSON and text formats
- **Extensible Design**: Easy to extend with additional entity types and relationships

## 📋 Prerequisites

- Python 3.8+
- Neo4j Database (4.0+)
- pip package manager

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd KGs
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Install Neo4j**:
   - Download from [Neo4j Download Center](https://neo4j.com/download/)
   - Or use Docker: `docker run -p7474:7474 -p7687:7687 neo4j:latest`

4. **Set up environment variables** (optional):
```bash
# Create .env file
cat > .env << EOF
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
EOF
```

## 🏃‍♂️ Quick Start

1. **Start Neo4j database**:
```bash
# Using Docker
docker run -p7474:7474 -p7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest

# Or start your local Neo4j instance
```

2. **Run the demo**:
```bash
python main.py
```

This will:
- Connect to Neo4j
- Create database schema
- Generate sample infrastructure data
- Demonstrate various query capabilities
- Export data for LLM consumption

## 📊 Usage Examples

### Basic Knowledge Graph Operations

```python
from kg.database import Neo4jKnowledgeGraph
from kg.data_generator import InfrastructureDataGenerator
from kg.llm_interface import KnowledgeGraphLLMInterface

# Initialize knowledge graph
kg = Neo4jKnowledgeGraph()

# Generate sample data
generator = InfrastructureDataGenerator(kg)
generator.populate_database()

# Initialize LLM interface
llm_interface = KnowledgeGraphLLMInterface(kg)
```

### Query Infrastructure Topology

```python
# Get topology summary
summary = llm_interface.get_topology_summary()
print(f"Total entities: {summary['infrastructure_overview']['total_entities']}")

# Get container to network mapping
containers = kg.query_entities_by_type(EntityType.CONTAINER)
container_id = containers[0]['id']
mapping = llm_interface.get_container_to_network_mapping(container_id)
```

### Natural Language Queries

```python
# Process natural language queries
response = llm_interface.query_natural_language("What is the topology overview?")
response = llm_interface.query_natural_language("Show me container to network mapping")
response = llm_interface.query_natural_language("What are the server resources?")
```

### Export for LLM Training

```python
# Export as JSON
json_data = llm_interface.export_for_llm_training("json")
with open("kg_export.json", "w") as f:
    f.write(json_data)

# Export as text
text_data = llm_interface.export_for_llm_training("text")
with open("kg_export.txt", "w") as f:
    f.write(text_data)
```

## 🔍 Advanced Queries

### Cypher Queries

The system provides useful Cypher queries for direct Neo4j interaction:

```cypher
-- Find all containers and their hosting path to physical servers
MATCH path = (c:Container)-[*]->(s:Server)
RETURN c.name as container, s.hostname as server, 
       [node in nodes(path) | node.name] as path_names
LIMIT 5

-- Get VLAN connectivity overview
MATCH (v:VLAN)-[r]-(e:Entity)
RETURN v.name as vlan, v.vlan_id as vlan_id, 
       count(e) as connected_entities,
       collect(DISTINCT labels(e)[1]) as entity_types

-- Get resource utilization summary by server
MATCH (s:Server)
OPTIONAL MATCH (s)-[:HOSTS]->(vm:VirtualMachine)
RETURN s.hostname as server, s.cpu_cores as server_cpu, s.memory_gb as server_memory,
       count(vm) as vm_count, sum(vm.cpu_cores) as allocated_cpu, sum(vm.memory_gb) as allocated_memory
```

### Python API

```python
# Get entity details
entity = kg.get_entity("entity-id")

# Find path between entities
path = kg.get_topology_path("source-id", "target-id")

# Get entity neighbors
neighbors = kg.get_entity_neighbors("entity-id")

# Search entities
results = kg.search_entities("production")

# Get database statistics
stats = kg.get_statistics()
```

## 🧠 LLM Integration

The system is designed for LLM consumption with several key features:

### Structured Data Export
- **JSON Format**: Complete graph structure with entities and relationships
- **Text Format**: Human-readable infrastructure descriptions
- **Metadata**: Timestamps, statistics, and context information

### Natural Language Interface
- Process queries in natural language
- Extract intent and provide relevant data
- Support for common infrastructure questions

### Context-Aware Responses
- Entity-specific context with relationships
- Path analysis between infrastructure components
- Security and resource utilization context

## 📁 Project Structure

```
KGs/
├── kg/
│   ├── __init__.py          # Package initialization
│   ├── models.py            # Pydantic models for entities
│   ├── database.py          # Neo4j database interface
│   ├── data_generator.py    # Sample data generation
│   └── llm_interface.py     # LLM consumption interface
├── main.py                  # Main demo script
├── config.py               # Configuration settings
├── setup.py                # Package setup
└── README.md               # This file
```

## ⚙️ Configuration

The system uses environment variables for configuration:

```python
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# Data Generation
SWITCH_COUNT=3
PORTS_PER_SWITCH=24
VLAN_COUNT=10
SERVER_COUNT=5
VMS_PER_SERVER=10
PODS_PER_VM=100
```

## 🔧 Customization

### Adding New Entity Types

1. **Define the model** in `kg/models.py`:
```python
class LoadBalancer(BaseEntity):
    type: EntityType = Field(default=EntityType.LOAD_BALANCER, const=True)
    algorithm: Optional[str] = Field(None, description="Load balancing algorithm")
    # ... additional fields
```

2. **Update the database schema** in `kg/database.py`:
```python
def setup_constraints_and_indexes(self):
    # Add constraint for new entity type
    constraints.append("CREATE CONSTRAINT lb_id IF NOT EXISTS FOR (lb:LoadBalancer) REQUIRE lb.id IS UNIQUE")
```

3. **Add data generation** in `kg/data_generator.py`:
```python
def create_load_balancers(self, count: int = 2) -> List[LoadBalancer]:
    # Implementation for generating load balancers
```

### Extending Relationships

Add new relationship types in `kg/models.py`:
```python
class RelationshipType(str, Enum):
    # ... existing types
    LOAD_BALANCES = "LOAD_BALANCES"
    MONITORS = "MONITORS"
```

## 🧪 Testing

Run the test suite:
```bash
# Set test environment
export ENVIRONMENT=testing

# Run tests
python -m pytest tests/
```

## 🐛 Troubleshooting

### Connection Issues
- Ensure Neo4j is running on the correct port
- Check username/password credentials
- Verify network connectivity

### Memory Issues
- Reduce data generation parameters for large datasets
- Increase Neo4j memory allocation
- Use database pagination for large queries

### Performance Optimization
- Create appropriate indexes for frequently queried properties
- Use `LIMIT` clauses for large result sets
- Consider database partitioning for very large datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📚 Documentation

### 📖 Complete Documentation Suite

This project includes comprehensive documentation for all skill levels:

- **[📚 Documentation Index](docs/README.md)** - Start here for guided documentation navigation
- **[🚀 Getting Started Guide](docs/GETTING_STARTED.md)** - Step-by-step tutorial (30 min)
- **[📚 API Reference](docs/API_REFERENCE.md)** - Complete API documentation
- **[📋 Examples & Use Cases](docs/EXAMPLES.md)** - Practical code examples
- **[🔧 Troubleshooting Guide](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[🚀 Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment strategies
- **[🎨 Visualization Guide](VISUALIZATION_GUIDE.md)** - Complete visualization documentation

### 🎯 Quick Start Documentation

- **New users**: Start with [Getting Started Guide](docs/GETTING_STARTED.md)
- **Developers**: Jump to [API Reference](docs/API_REFERENCE.md)
- **DevOps**: Check out [Deployment Guide](docs/DEPLOYMENT.md)
- **Issues**: See [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

### 🔗 External Resources

- **Neo4j Documentation**: [https://neo4j.com/docs/](https://neo4j.com/docs/)
- **Cypher Query Language**: [https://neo4j.com/docs/cypher-manual/](https://neo4j.com/docs/cypher-manual/)
- **Pydantic Models**: [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏷️ Version

Current version: 0.1.0

## 📧 Support

For support and questions, please open an issue in the GitHub repository.

---

**Note**: This system is designed as a foundation for infrastructure knowledge graphs. Extend and customize it according to your specific use case and requirements. 