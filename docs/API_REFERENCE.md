# 📚 API Reference

## Overview

This document provides complete API documentation for the Network Infrastructure Knowledge Graph system. All classes, methods, and functions are documented with parameters, return values, and examples.

## 🏗️ Architecture

```
kg/
├── models.py           # Entity and relationship models
├── database.py         # Neo4j database operations
├── data_generator.py   # Sample data generation
├── llm_interface.py    # LLM integration interface
└── visualization.py    # Graph visualization methods
```

---

## 🎯 Core Classes

### `Neo4jKnowledgeGraph`
*File: `kg/database.py`*

Main interface for all database operations.

#### Constructor
```python
Neo4jKnowledgeGraph(
    uri: str = None,
    username: str = None,
    password: str = None,
    database: str = "neo4j"
)
```

**Parameters:**
- `uri` (str): Neo4j connection URI (default: from config)
- `username` (str): Database username (default: from config)
- `password` (str): Database password (default: from config)
- `database` (str): Database name (default: "neo4j")

**Example:**
```python
from kg.database import Neo4jKnowledgeGraph

# Using default configuration
kg = Neo4jKnowledgeGraph()

# Using custom connection
kg = Neo4jKnowledgeGraph(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="mypassword"
)
```

#### Core Methods

##### `setup_constraints_and_indexes()`
Creates database constraints and indexes for optimal performance.

**Returns:** `None`

**Example:**
```python
kg.setup_constraints_and_indexes()
```

##### `create_entity(entity: BaseEntity) -> Dict[str, Any]`
Creates a new entity in the database.

**Parameters:**
- `entity` (BaseEntity): Entity object to create

**Returns:** `Dict[str, Any]` - Created entity data

**Example:**
```python
from kg.models import NetworkSwitch

switch = NetworkSwitch(
    name="Core-Switch-01",
    hostname="switch-01.example.com",
    ip_address="192.168.1.1",
    port_count=48
)
created_entity = kg.create_entity(switch)
```

##### `create_relationship(source_id: str, target_id: str, relationship_type: RelationshipType, properties: Dict = None) -> Dict[str, Any]`
Creates a relationship between two entities.

**Parameters:**
- `source_id` (str): Source entity ID
- `target_id` (str): Target entity ID
- `relationship_type` (RelationshipType): Type of relationship
- `properties` (Dict, optional): Additional relationship properties

**Returns:** `Dict[str, Any]` - Created relationship data

**Example:**
```python
from kg.models import RelationshipType

rel = kg.create_relationship(
    source_id="switch-01",
    target_id="port-01",
    relationship_type=RelationshipType.CONTAINS,
    properties={"connection_type": "physical"}
)
```

##### `get_entity(entity_id: str) -> Optional[Dict[str, Any]]`
Retrieves an entity by ID.

**Parameters:**
- `entity_id` (str): Entity ID to retrieve

**Returns:** `Optional[Dict[str, Any]]` - Entity data or None

**Example:**
```python
entity = kg.get_entity("switch-01")
if entity:
    print(f"Found entity: {entity['name']}")
```

##### `query_entities_by_type(entity_type: EntityType) -> List[Dict[str, Any]]`
Retrieves all entities of a specific type.

**Parameters:**
- `entity_type` (EntityType): Type of entities to retrieve

**Returns:** `List[Dict[str, Any]]` - List of entity data

**Example:**
```python
from kg.models import EntityType

servers = kg.query_entities_by_type(EntityType.SERVER)
print(f"Found {len(servers)} servers")
```

##### `get_topology_path(source_id: str, target_id: str) -> Optional[List[Dict[str, Any]]]`
Finds the shortest path between two entities.

**Parameters:**
- `source_id` (str): Source entity ID
- `target_id` (str): Target entity ID

**Returns:** `Optional[List[Dict[str, Any]]]` - Path data or None

**Example:**
```python
path = kg.get_topology_path("container-01", "server-01")
if path:
    print(f"Path length: {len(path)} hops")
```

##### `get_entity_neighbors(entity_id: str) -> List[Dict[str, Any]]`
Gets all directly connected entities.

**Parameters:**
- `entity_id` (str): Entity ID to get neighbors for

**Returns:** `List[Dict[str, Any]]` - List of neighbor entities

**Example:**
```python
neighbors = kg.get_entity_neighbors("server-01")
print(f"Server has {len(neighbors)} neighbors")
```

##### `search_entities(search_term: str) -> List[Dict[str, Any]]`
Searches entities by name or properties.

**Parameters:**
- `search_term` (str): Term to search for

**Returns:** `List[Dict[str, Any]]` - Matching entities

**Example:**
```python
results = kg.search_entities("production")
print(f"Found {len(results)} production entities")
```

##### `get_statistics() -> Dict[str, Any]`
Gets database statistics and counts.

**Returns:** `Dict[str, Any]` - Database statistics

**Example:**
```python
stats = kg.get_statistics()
print(f"Total entities: {stats['total_entities']}")
print(f"Total relationships: {stats['total_relationships']}")
```

##### `execute_query(query: str, parameters: Dict = None) -> List[Dict[str, Any]]`
Executes a raw Cypher query.

**Parameters:**
- `query` (str): Cypher query string
- `parameters` (Dict, optional): Query parameters

**Returns:** `List[Dict[str, Any]]` - Query results

**Example:**
```python
query = "MATCH (s:Server) WHERE s.cpu_cores > $min_cores RETURN s"
results = kg.execute_query(query, {"min_cores": 8})
```

---

## 🤖 LLM Interface

### `KnowledgeGraphLLMInterface`
*File: `kg/llm_interface.py`*

Interface for LLM consumption of knowledge graph data.

#### Constructor
```python
KnowledgeGraphLLMInterface(knowledge_graph: Neo4jKnowledgeGraph)
```

**Parameters:**
- `knowledge_graph` (Neo4jKnowledgeGraph): Knowledge graph instance

**Example:**
```python
from kg.llm_interface import KnowledgeGraphLLMInterface

kg = Neo4jKnowledgeGraph()
llm = KnowledgeGraphLLMInterface(kg)
```

#### Methods

##### `query_natural_language(question: str) -> str`
Processes natural language queries and returns structured responses.

**Parameters:**
- `question` (str): Natural language question

**Returns:** `str` - Formatted response

**Supported Questions:**
- "What is the topology overview?"
- "Show me server resources"
- "What are the container details?"
- "Show me the network overview"
- "What are the security contexts?"

**Example:**
```python
response = llm.query_natural_language("What is the topology overview?")
print(response)
```

##### `export_for_llm_training(format_type: str = "json") -> str`
Exports knowledge graph data for LLM training.

**Parameters:**
- `format_type` (str): Export format ("json" or "text")

**Returns:** `str` - Exported data

**Example:**
```python
# Export as JSON
json_data = llm.export_for_llm_training("json")

# Export as text
text_data = llm.export_for_llm_training("text")
```

##### `get_topology_summary() -> Dict[str, Any]`
Gets comprehensive topology summary.

**Returns:** `Dict[str, Any]` - Topology summary

**Example:**
```python
summary = llm.get_topology_summary()
print(f"Infrastructure has {summary['infrastructure_overview']['total_entities']} entities")
```

##### `get_container_to_network_mapping(container_id: str) -> Dict[str, Any]`
Maps container to its network path.

**Parameters:**
- `container_id` (str): Container ID

**Returns:** `Dict[str, Any]` - Network mapping

**Example:**
```python
mapping = llm.get_container_to_network_mapping("container-01")
print(f"Container network path: {mapping['network_path']}")
```

---

## 🎨 Visualization

### `GraphVisualizer`
*File: `kg/visualization.py`*

Handles all graph visualization operations.

#### Constructor
```python
GraphVisualizer(knowledge_graph: Neo4jKnowledgeGraph)
```

**Parameters:**
- `knowledge_graph` (Neo4jKnowledgeGraph): Knowledge graph instance

**Example:**
```python
from kg.visualization import GraphVisualizer

kg = Neo4jKnowledgeGraph()
viz = GraphVisualizer(kg)
```

#### Methods

##### `create_pyvis_network(filter_entities: List[str] = None, output_file: str = "network.html") -> str`
Creates interactive HTML network visualization.

**Parameters:**
- `filter_entities` (List[str], optional): Entity types to include
- `output_file` (str): Output HTML file path

**Returns:** `str` - Path to created file

**Example:**
```python
# Create full network
viz.create_pyvis_network(output_file="full_network.html")

# Create filtered network
viz.create_pyvis_network(
    filter_entities=["Server", "VirtualMachine"],
    output_file="servers_only.html"
)
```

##### `create_matplotlib_static(filter_entities: List[str] = None, output_file: str = "network.png") -> str`
Creates static PNG network visualization.

**Parameters:**
- `filter_entities` (List[str], optional): Entity types to include
- `output_file` (str): Output PNG file path

**Returns:** `str` - Path to created file

**Example:**
```python
viz.create_matplotlib_static(output_file="topology.png")
```

##### `create_plotly_network(filter_entities: List[str] = None, layout_algorithm: str = "spring") -> Any`
Creates interactive Plotly network visualization.

**Parameters:**
- `filter_entities` (List[str], optional): Entity types to include
- `layout_algorithm` (str): Layout algorithm ("spring", "circular", "kamada_kawai")

**Returns:** `plotly.graph_objects.Figure` - Plotly figure object

**Example:**
```python
fig = viz.create_plotly_network(layout_algorithm="circular")
fig.show()
```

##### `create_hierarchy_chart(output_file: str = "hierarchy.html") -> str`
Creates entity hierarchy bar chart.

**Parameters:**
- `output_file` (str): Output HTML file path

**Returns:** `str` - Path to created file

**Example:**
```python
viz.create_hierarchy_chart("entity_distribution.html")
```

---

## 🎲 Data Generation

### `InfrastructureDataGenerator`
*File: `kg/data_generator.py`*

Generates realistic infrastructure data for testing and demonstration.

#### Constructor
```python
InfrastructureDataGenerator(knowledge_graph: Neo4jKnowledgeGraph)
```

**Parameters:**
- `knowledge_graph` (Neo4jKnowledgeGraph): Knowledge graph instance

**Example:**
```python
from kg.data_generator import InfrastructureDataGenerator

kg = Neo4jKnowledgeGraph()
generator = InfrastructureDataGenerator(kg)
```

#### Methods

##### `populate_database() -> Dict[str, int]`
Populates the database with a complete infrastructure topology.

**Returns:** `Dict[str, int]` - Count of created entities by type

**Example:**
```python
counts = generator.populate_database()
print(f"Created {counts['servers']} servers")
print(f"Created {counts['containers']} containers")
```

##### `create_network_switches(count: int = 3) -> List[NetworkSwitch]`
Creates network switches.

**Parameters:**
- `count` (int): Number of switches to create

**Returns:** `List[NetworkSwitch]` - Created switches

**Example:**
```python
switches = generator.create_network_switches(count=5)
```

##### `create_servers(count: int = 5) -> List[Server]`
Creates physical servers.

**Parameters:**
- `count` (int): Number of servers to create

**Returns:** `List[Server]` - Created servers

**Example:**
```python
servers = generator.create_servers(count=10)
```

---

## 📊 Entity Models

### Base Entity Classes
*File: `kg/models.py`*

All entity types inherit from `BaseEntity`:

```python
class BaseEntity(BaseModel):
    id: str = Field(description="Unique identifier")
    name: str = Field(description="Human-readable name")
    description: Optional[str] = Field(None, description="Optional description")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    type: EntityType = Field(description="Entity type")
    labels: List[str] = Field(default_factory=list)
    properties: Dict[str, Any] = Field(default_factory=dict)
```

### Entity Types

#### `NetworkSwitch`
Represents a network switch.

**Key Fields:**
- `hostname: str` - Switch hostname
- `ip_address: str` - Management IP
- `port_count: int` - Number of ports
- `model: str` - Switch model
- `firmware_version: str` - Firmware version

**Example:**
```python
switch = NetworkSwitch(
    name="Core-Switch-01",
    hostname="switch-01.example.com",
    ip_address="192.168.1.1",
    port_count=48,
    model="Cisco-2960X",
    firmware_version="15.2.4"
)
```

#### `Server`
Represents a physical server.

**Key Fields:**
- `hostname: str` - Server hostname
- `cpu_cores: int` - CPU core count
- `memory_gb: int` - Memory in GB
- `storage_gb: int` - Storage in GB
- `operating_system: str` - OS name

**Example:**
```python
server = Server(
    name="Web-Server-01",
    hostname="web-01.example.com",
    cpu_cores=16,
    memory_gb=64,
    storage_gb=1000,
    operating_system="Ubuntu 20.04"
)
```

#### `Container`
Represents a container.

**Key Fields:**
- `image: str` - Container image
- `cpu_cores: float` - CPU allocation
- `memory_mb: int` - Memory in MB
- `status: str` - Container status

**Example:**
```python
container = Container(
    name="nginx-web-01",
    image="nginx:1.21",
    cpu_cores=0.5,
    memory_mb=256,
    status="running"
)
```

### Relationship Types

```python
class RelationshipType(str, Enum):
    CONNECTED_TO = "CONNECTED_TO"
    HOSTS = "HOSTS"
    RUNS_ON = "RUNS_ON"
    BELONGS_TO = "BELONGS_TO"
    CONTAINS = "CONTAINS"
    DEPLOYED_ON = "DEPLOYED_ON"
    PART_OF = "PART_OF"
```

---

## 🔧 Configuration

### Environment Variables
*File: `config.py`*

```python
# Neo4j Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "password"

# Data Generation Parameters
SWITCH_COUNT = 3
PORTS_PER_SWITCH = 24
VLAN_COUNT = 10
SERVER_COUNT = 5
VMS_PER_SERVER = 10
PODS_PER_VM = 100
CONTAINERS_PER_POD = 2
```

### Custom Configuration

```python
import os
from config import *

# Override configuration
os.environ['NEO4J_URI'] = 'bolt://production-db:7687'
os.environ['NEO4J_PASSWORD'] = 'secure-password'
```

---

## 🚨 Error Handling

### Common Exceptions

#### `Neo4jConnectionError`
Raised when database connection fails.

```python
try:
    kg = Neo4jKnowledgeGraph()
except Neo4jConnectionError as e:
    print(f"Database connection failed: {e}")
```

#### `EntityNotFoundError`
Raised when requested entity doesn't exist.

```python
try:
    entity = kg.get_entity("non-existent-id")
except EntityNotFoundError as e:
    print(f"Entity not found: {e}")
```

#### `ValidationError`
Raised when entity data is invalid.

```python
try:
    server = Server(name="", cpu_cores=-1)  # Invalid data
except ValidationError as e:
    print(f"Validation error: {e}")
```

---

## 📈 Performance Tips

### Efficient Queries

```python
# Good: Use indexed properties
results = kg.execute_query("MATCH (s:Server) WHERE s.id = $id RETURN s", {"id": "server-01"})

# Bad: Avoid non-indexed property scans
results = kg.execute_query("MATCH (s:Server) WHERE s.description CONTAINS 'production' RETURN s")
```

### Batch Operations

```python
# Create multiple entities efficiently
entities = [server1, server2, server3]
for entity in entities:
    kg.create_entity(entity)
```

### Memory Management

```python
# Use pagination for large result sets
query = "MATCH (n:Container) RETURN n SKIP $skip LIMIT $limit"
results = kg.execute_query(query, {"skip": 0, "limit": 1000})
```

---

## 🧪 Testing

### Unit Tests

```python
import unittest
from kg.database import Neo4jKnowledgeGraph
from kg.models import Server

class TestKnowledgeGraph(unittest.TestCase):
    def setUp(self):
        self.kg = Neo4jKnowledgeGraph()
    
    def test_create_entity(self):
        server = Server(name="test-server", hostname="test.com", cpu_cores=4)
        result = self.kg.create_entity(server)
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], "test-server")
```

### Integration Tests

```python
def test_full_workflow():
    kg = Neo4jKnowledgeGraph()
    generator = InfrastructureDataGenerator(kg)
    
    # Generate data
    counts = generator.populate_database()
    assert counts['servers'] > 0
    
    # Test queries
    servers = kg.query_entities_by_type(EntityType.SERVER)
    assert len(servers) == counts['servers']
```

---

## 🔍 Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now all database operations will be logged
kg = Neo4jKnowledgeGraph()
```

### Query Profiling

```python
# Profile slow queries
query = "MATCH (n)-[r]->(m) RETURN count(*)"
results = kg.execute_query(f"PROFILE {query}")
```

### Database Inspection

```python
# Check database state
stats = kg.get_statistics()
print(f"Entities: {stats['total_entities']}")
print(f"Relationships: {stats['total_relationships']}")

# List all entity types
query = "MATCH (n) RETURN DISTINCT labels(n) as types"
types = kg.execute_query(query)
```

---

## 📝 Examples

### Complete Workflow Example

```python
from kg.database import Neo4jKnowledgeGraph
from kg.data_generator import InfrastructureDataGenerator
from kg.llm_interface import KnowledgeGraphLLMInterface
from kg.visualization import GraphVisualizer

# Initialize system
kg = Neo4jKnowledgeGraph()
generator = InfrastructureDataGenerator(kg)
llm = KnowledgeGraphLLMInterface(kg)
viz = GraphVisualizer(kg)

# Generate data
counts = generator.populate_database()
print(f"Created infrastructure with {sum(counts.values())} entities")

# Query data
servers = kg.query_entities_by_type(EntityType.SERVER)
print(f"Found {len(servers)} servers")

# Natural language query
response = llm.query_natural_language("What is the topology overview?")
print(response)

# Create visualization
viz.create_pyvis_network(output_file="my_network.html")

# Export for LLM
json_data = llm.export_for_llm_training("json")
with open("export.json", "w") as f:
    f.write(json_data)
```

### Custom Entity Creation

```python
from kg.models import BaseEntity, EntityType

class LoadBalancer(BaseEntity):
    type: EntityType = Field(default=EntityType.LOAD_BALANCER, const=True)
    algorithm: str = Field(description="Load balancing algorithm")
    backend_servers: List[str] = Field(description="Backend server IDs")

# Create and save
lb = LoadBalancer(
    name="Main-LB",
    algorithm="round_robin",
    backend_servers=["server-01", "server-02"]
)
kg.create_entity(lb)
```

---

This API reference provides comprehensive documentation for all available functionality. For more examples and tutorials, see the other documentation files in the `docs/` directory. 