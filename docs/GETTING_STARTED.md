# 🚀 Getting Started Guide

## Welcome to the Network Infrastructure Knowledge Graph!

This guide will walk you through setting up and using the knowledge graph system from scratch. Perfect for beginners who want to understand how everything works together.

## 🎯 What You'll Learn

By the end of this guide, you'll be able to:
- Set up the complete system locally
- Generate your first knowledge graph
- Query infrastructure data
- Create visualizations
- Use the web dashboard
- Export data for AI/LLM use

## 📋 Prerequisites

Before we begin, make sure you have:
- **Python 3.8+** installed
- **Basic terminal/command line knowledge**
- **About 30 minutes** to complete this guide

## 🔧 Step 1: System Setup

### 1.1 Install Neo4j Database

**Option A: Using Docker (Recommended)**
```bash
# Pull and run Neo4j container
docker run -d \
  --name neo4j-kg \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  -v neo4j_data:/data \
  neo4j:latest

# Wait for startup (about 30 seconds)
```

**Option B: Native Installation**
1. Download Neo4j from [neo4j.com/download](https://neo4j.com/download)
2. Follow installation instructions for your OS
3. Start Neo4j and set password to `password`

### 1.2 Verify Neo4j Installation

Visit [http://localhost:7474](http://localhost:7474) in your browser:
- Username: `neo4j`
- Password: `password`

You should see the Neo4j Browser interface.

### 1.3 Set Up Python Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd KGs

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🎮 Step 2: Your First Knowledge Graph

### 2.1 Run the Demo

```bash
# Make sure Neo4j is running, then:
python main.py
```

**What happens:**
1. ✅ Connects to Neo4j database
2. ✅ Creates database schema (constraints and indexes)
3. ✅ Generates sample infrastructure data
4. ✅ Creates ~500+ entities and relationships
5. ✅ Demonstrates various queries
6. ✅ Exports data for LLM use

### 2.2 Expected Output

```
🔗 Connecting to Neo4j...
✅ Connected to Neo4j at bolt://localhost:7687

🏗️ Setting up database schema...
✅ Database schema created successfully

🎲 Generating sample infrastructure data...
✅ Created 3 network switches
✅ Created 72 network ports
✅ Created 10 VLANs
✅ Created 5 servers
✅ Created 50 virtual machines
✅ Created 500 Kubernetes pods
✅ Created 1000 containers
✅ Total entities: 1640, relationships: 1689

🔍 Demonstrating queries...
[Query results shown here]

📊 Exporting data for LLM training...
✅ Exported to infrastructure_kg_export.json
✅ Exported to infrastructure_kg_export.txt
```

### 2.3 Explore Your Data

**In Neo4j Browser** ([http://localhost:7474](http://localhost:7474)):

```cypher
# See all entity types
MATCH (n) RETURN DISTINCT labels(n) as EntityTypes

# View a sample of each entity type
MATCH (n:NetworkSwitch) RETURN n LIMIT 3
MATCH (n:Server) RETURN n LIMIT 3
MATCH (n:Container) RETURN n LIMIT 5
```

## 📊 Step 3: Visualizations

### 3.1 Generate All Visualizations

```bash
python demo_visualizations.py
```

This creates multiple visualization files in the `visualizations/` directory:
- `interactive_network.html` - Interactive network graph
- `topology_static.png` - Static network image
- `hierarchy_chart.html` - Entity distribution chart
- `filtered_*.html` - Layer-specific views

### 3.2 View Interactive Network

```bash
# Open in your browser
open visualizations/interactive_network.html
```

**Features to try:**
- **Click and drag** nodes to reorganize
- **Hover** over nodes to see details
- **Zoom** in/out with mouse wheel
- **Pan** by dragging empty space

### 3.3 Start the Web Dashboard

```bash
streamlit run streamlit_app.py
```

Visit [http://localhost:8501](http://localhost:8501) to see:
- Real-time interactive network graphs
- Filter controls for entity types
- Multiple layout algorithms
- Statistics overview
- Layer-specific views

## 🤖 Step 4: LLM Integration

### 4.1 Natural Language Queries

```python
# In Python shell or script
from kg.database import Neo4jKnowledgeGraph
from kg.llm_interface import KnowledgeGraphLLMInterface

# Initialize
kg = Neo4jKnowledgeGraph()
llm = KnowledgeGraphLLMInterface(kg)

# Ask questions in natural language
response = llm.query_natural_language("What is the topology overview?")
print(response)

response = llm.query_natural_language("Show me server resources")
print(response)
```

### 4.2 Export Data for Training

```python
# Export as JSON for structured AI consumption
json_data = llm.export_for_llm_training("json")
with open("my_export.json", "w") as f:
    f.write(json_data)

# Export as text for human readability
text_data = llm.export_for_llm_training("text")
with open("my_export.txt", "w") as f:
    f.write(text_data)
```

## 🔍 Step 5: Advanced Queries

### 5.1 Python API Examples

```python
from kg.database import Neo4jKnowledgeGraph
from kg.models import EntityType

kg = Neo4jKnowledgeGraph()

# Get all servers
servers = kg.query_entities_by_type(EntityType.SERVER)
print(f"Found {len(servers)} servers")

# Find path between entities
containers = kg.query_entities_by_type(EntityType.CONTAINER)
servers = kg.query_entities_by_type(EntityType.SERVER)

if containers and servers:
    path = kg.get_topology_path(containers[0]['id'], servers[0]['id'])
    print(f"Path from container to server: {path}")

# Get entity neighbors
neighbors = kg.get_entity_neighbors(servers[0]['id'])
print(f"Server neighbors: {len(neighbors)}")
```

### 5.2 Cypher Query Examples

In Neo4j Browser:

```cypher
-- Find containers running on specific servers
MATCH (c:Container)-[*]->(s:Server)
WHERE s.hostname CONTAINS 'prod'
RETURN c.name, s.hostname
LIMIT 10

-- Get VLAN utilization
MATCH (v:VLAN)-[]->(entity)
RETURN v.name, v.vlan_id, count(entity) as connected_count
ORDER BY connected_count DESC

-- Find high-resource containers
MATCH (c:Container)
WHERE c.memory_mb > 512
RETURN c.name, c.memory_mb, c.cpu_cores
ORDER BY c.memory_mb DESC
```

## 🎨 Step 6: Customization

### 6.1 Modify Data Generation

Edit `config.py` to change the scale:

```python
# Generate more entities
SWITCH_COUNT = 5        # Default: 3
SERVER_COUNT = 10       # Default: 5
VMS_PER_SERVER = 20     # Default: 10
```

Then regenerate:
```bash
python main.py
```

### 6.2 Add Custom Queries

Create a new file `my_queries.py`:

```python
from kg.database import Neo4jKnowledgeGraph

kg = Neo4jKnowledgeGraph()

# Custom query function
def find_production_containers():
    query = """
    MATCH (c:Container)-[*]->(s:Server)
    WHERE s.hostname CONTAINS 'prod'
    RETURN c.name, c.image, s.hostname
    """
    return kg.execute_query(query)

# Run your query
results = find_production_containers()
for record in results:
    print(f"Container: {record['c.name']}, Server: {record['s.hostname']}")
```

### 6.3 Create Custom Visualizations

```python
from kg.visualization import GraphVisualizer
from kg.database import Neo4jKnowledgeGraph

kg = Neo4jKnowledgeGraph()
viz = GraphVisualizer(kg)

# Create a servers-only visualization
viz.create_pyvis_network(
    filter_entities=['Server', 'VirtualMachine'],
    output_file='servers_only.html'
)
```

## 🐛 Common Issues & Solutions

### Problem: "Connection refused" error

**Solution:**
```bash
# Check if Neo4j is running
docker ps | grep neo4j

# If not running, start it
docker start neo4j-kg

# Or restart the container
docker restart neo4j-kg
```

### Problem: "Authentication failed"

**Solution:**
Check your credentials in `config.py`:
```python
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "password"  # Make sure this matches your Neo4j password
```

### Problem: Streamlit app shows errors

**Solution:**
```bash
# Make sure database is populated first
python main.py

# Then run Streamlit
streamlit run streamlit_app.py
```

### Problem: Visualizations are empty

**Solution:**
Make sure you have data in the database:
```bash
# Check entity count
python -c "from kg.database import Neo4jKnowledgeGraph; kg = Neo4jKnowledgeGraph(); print(kg.get_statistics())"
```

## 🎉 Next Steps

Congratulations! You now have a fully functional knowledge graph system. Here's what to explore next:

1. **📖 Read the API Reference** - Learn about all available methods
2. **🎨 Visualization Guide** - Master all visualization options
3. **🔧 Customization Examples** - Add your own entity types
4. **🚀 Deployment Guide** - Deploy to production
5. **🤝 Contributing** - Help improve the project

## 📚 Quick Reference

### Essential Commands
```bash
# Start Neo4j
docker start neo4j-kg

# Generate data
python main.py

# Create visualizations
python demo_visualizations.py

# Run dashboard
streamlit run streamlit_app.py

# Open Neo4j browser
open http://localhost:7474
```

### Key Files
- `main.py` - Main demonstration script
- `config.py` - Configuration settings
- `kg/database.py` - Database operations
- `kg/models.py` - Entity definitions
- `kg/visualization.py` - Visualization methods
- `streamlit_app.py` - Web dashboard

### Important URLs
- Neo4j Browser: http://localhost:7474
- Streamlit Dashboard: http://localhost:8501

---

**Need Help?** Check out the other documentation files:
- `API_REFERENCE.md` - Complete API documentation
- `TROUBLESHOOTING.md` - Common issues and solutions
- `EXAMPLES.md` - More code examples and use cases 