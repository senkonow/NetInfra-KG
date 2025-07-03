# 🔧 Troubleshooting Guide

## Overview

This guide helps you resolve common issues when working with the Network Infrastructure Knowledge Graph system. Issues are organized by category with step-by-step solutions.

---

## 🔌 Database Connection Issues

### Problem: "Connection refused" or "ServiceUnavailable"

**Symptoms:**
- Error messages about connection refused
- Unable to connect to Neo4j database
- ServiceUnavailable exceptions

**Solutions:**

#### 1. Check Neo4j Status
```bash
# If using Docker
docker ps | grep neo4j

# If no container is running
docker start neo4j-kg

# Check container logs
docker logs neo4j-kg
```

#### 2. Verify Neo4j is Running
```bash
# Test connection manually
curl -I http://localhost:7474

# Should return HTTP 200 OK
```

#### 3. Check Port Availability
```bash
# Check if ports are in use
lsof -i :7474  # Neo4j HTTP
lsof -i :7687  # Neo4j Bolt

# Kill processes if needed
kill -9 <PID>
```

#### 4. Restart Neo4j
```bash
# Docker restart
docker restart neo4j-kg

# Or stop and start fresh
docker stop neo4j-kg
docker rm neo4j-kg
docker run -d --name neo4j-kg -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password neo4j:latest
```

### Problem: "Authentication failed"

**Symptoms:**
- Invalid username/password errors
- Authentication failed messages

**Solutions:**

#### 1. Check Configuration
```python
# In config.py, verify:
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "password"  # Must match your Neo4j password
```

#### 2. Reset Neo4j Password
```bash
# Using Docker
docker exec -it neo4j-kg cypher-shell -u neo4j -p neo4j
# Then run: ALTER USER neo4j SET PASSWORD 'password';
```

#### 3. Environment Variables
```bash
# Set environment variables
export NEO4J_USERNAME=neo4j
export NEO4J_PASSWORD=password
```

### Problem: "Database does not exist"

**Symptoms:**
- Database "neo4j" does not exist
- Cannot access specified database

**Solutions:**

#### 1. Use Default Database
```python
# In your code, use default database
kg = Neo4jKnowledgeGraph(database="neo4j")
```

#### 2. Create Database (Neo4j 4.0+)
```cypher
-- In Neo4j Browser
CREATE DATABASE mydb;
```

---

## 🐍 Python Environment Issues

### Problem: "ModuleNotFoundError"

**Symptoms:**
- Cannot import kg modules
- Module not found errors

**Solutions:**

#### 1. Install Dependencies
```bash
# Make sure you're in the project directory
cd KGs

# Install requirements
pip install -r requirements.txt

# Or install specific packages
pip install neo4j pydantic streamlit plotly pyvis networkx
```

#### 2. Check Python Path
```python
import sys
sys.path.append('/path/to/KGs')

# Or set PYTHONPATH
export PYTHONPATH=/path/to/KGs:$PYTHONPATH
```

#### 3. Activate Virtual Environment
```bash
# If using venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# If using conda
conda activate your-env
```

### Problem: "ImportError: cannot import name 'X'"

**Symptoms:**
- Specific imports fail
- Circular import errors

**Solutions:**

#### 1. Check Import Order
```python
# Correct order
from kg.database import Neo4jKnowledgeGraph
from kg.models import EntityType
from kg.data_generator import InfrastructureDataGenerator

# Avoid circular imports
```

#### 2. Use Absolute Imports
```python
# Instead of relative imports
from kg.database import Neo4jKnowledgeGraph
# Not: from .database import Neo4jKnowledgeGraph
```

---

## 📊 Data Generation Issues

### Problem: "No data generated" or "Empty database"

**Symptoms:**
- Statistics show 0 entities
- Visualizations are empty
- Queries return no results

**Solutions:**

#### 1. Check Data Generation
```python
from kg.database import Neo4jKnowledgeGraph
from kg.data_generator import InfrastructureDataGenerator

kg = Neo4jKnowledgeGraph()
generator = InfrastructureDataGenerator(kg)

# Clear database first
kg.execute_query("MATCH (n) DETACH DELETE n")

# Generate data
counts = generator.populate_database()
print(f"Generated: {counts}")
```

#### 2. Verify Database Schema
```python
# Check if constraints exist
kg.setup_constraints_and_indexes()
```

#### 3. Check Configuration
```python
# In config.py, ensure reasonable values
SWITCH_COUNT = 3        # Not 0
SERVER_COUNT = 5        # Not 0
VMS_PER_SERVER = 10     # Not 0
```

### Problem: "Validation errors during data generation"

**Symptoms:**
- Pydantic validation errors
- Invalid data format errors

**Solutions:**

#### 1. Check Entity Models
```python
# Make sure entity data is valid
from kg.models import Server

try:
    server = Server(
        name="test-server",
        hostname="test.example.com",
        cpu_cores=4,  # Must be positive integer
        memory_gb=8,  # Must be positive
        storage_gb=100,  # Must be positive
        operating_system="Ubuntu 20.04"
    )
except ValidationError as e:
    print(f"Validation error: {e}")
```

#### 2. Fix Data Types
```python
# Common fixes
cpu_cores = int(cpu_cores)  # Ensure integer
memory_gb = max(1, memory_gb)  # Ensure positive
ip_address = str(ip_address)  # Ensure string
```

---

## 🎨 Visualization Issues

### Problem: "KeyError: 'entities'" in Streamlit

**Symptoms:**
- Streamlit app crashes with KeyError
- Visualization shows error messages

**Solutions:**

#### 1. Check Data Retrieval Method
```python
# In kg/visualization.py, ensure graph_data has correct structure
def create_networkx_graph(self, filter_entities=None):
    graph_data = self.get_graph_data(filter_entities)
    
    # Debug: print structure
    print(f"Graph data keys: {graph_data.keys()}")
    
    # Check for correct key
    if 'entities' not in graph_data:
        print("Warning: 'entities' key not found in graph_data")
        return networkx.Graph()
```

#### 2. Fix Database Query
```python
# In get_graph_data method, ensure correct return format
def get_graph_data(self, filter_entities=None):
    # ... query logic ...
    
    return {
        'entities': entities,  # Make sure this key exists
        'relationships': relationships
    }
```

#### 3. Run Data Generation First
```bash
# Make sure database has data before starting Streamlit
python main.py
streamlit run streamlit_app.py
```

### Problem: "Empty visualizations"

**Symptoms:**
- Graphs show no nodes or edges
- Static images are blank

**Solutions:**

#### 1. Check Entity Count
```python
from kg.database import Neo4jKnowledgeGraph

kg = Neo4jKnowledgeGraph()
stats = kg.get_statistics()
print(f"Total entities: {stats['total_entities']}")

if stats['total_entities'] == 0:
    print("No entities found - run data generation first")
```

#### 2. Verify Filters
```python
# Check if filters are too restrictive
visualizer = GraphVisualizer(kg)
visualizer.create_pyvis_network(
    filter_entities=None,  # Remove filters to see all data
    output_file="debug_network.html"
)
```

### Problem: "Layout algorithms not working"

**Symptoms:**
- Nodes all appear in same position
- Layout looks messy or overlapping

**Solutions:**

#### 1. Try Different Algorithms
```python
# Test different layout algorithms
layouts = ['spring', 'circular', 'kamada_kawai', 'random']
for layout in layouts:
    try:
        fig = visualizer.create_plotly_network(layout_algorithm=layout)
        print(f"Layout {layout} works")
        break
    except Exception as e:
        print(f"Layout {layout} failed: {e}")
```

#### 2. Adjust Graph Size
```python
# For large graphs, use sampling
query = "MATCH (n) RETURN n LIMIT 100"  # Limit node count
```

---

## 🌐 Streamlit App Issues

### Problem: "Streamlit app won't start"

**Symptoms:**
- Command not found errors
- App fails to launch

**Solutions:**

#### 1. Install Streamlit
```bash
pip install streamlit

# Verify installation
streamlit --version
```

#### 2. Check File Path
```bash
# Make sure you're in the correct directory
cd /path/to/KGs
ls streamlit_app.py  # Should exist

# Run from correct location
streamlit run streamlit_app.py
```

#### 3. Check Port Availability
```bash
# Check if port 8501 is in use
lsof -i :8501

# Use different port if needed
streamlit run streamlit_app.py --server.port 8502
```

### Problem: "Streamlit shows errors or crashes"

**Symptoms:**
- App loads but shows error messages
- Frequent crashes or reloads

**Solutions:**

#### 1. Check Dependencies
```bash
# Make sure all dependencies are installed
pip install streamlit plotly pyvis networkx matplotlib
```

#### 2. Debug Mode
```python
# Add debug prints to streamlit_app.py
import streamlit as st

try:
    # Your visualization code
    pass
except Exception as e:
    st.error(f"Error: {e}")
    st.exception(e)  # Show full traceback
```

#### 3. Clear Cache
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/
```

---

## 💾 Data Export Issues

### Problem: "Export files are empty or corrupted"

**Symptoms:**
- JSON files are empty
- Text files contain errors
- Export process fails

**Solutions:**

#### 1. Check LLM Interface
```python
from kg.llm_interface import KnowledgeGraphLLMInterface

kg = Neo4jKnowledgeGraph()
llm = KnowledgeGraphLLMInterface(kg)

# Test export
try:
    data = llm.export_for_llm_training("json")
    print(f"Export length: {len(data)}")
except Exception as e:
    print(f"Export failed: {e}")
```

#### 2. Verify Data Exists
```python
# Check if database has data
stats = kg.get_statistics()
if stats['total_entities'] == 0:
    print("No data to export - generate data first")
    # Run: python main.py
```

#### 3. Check File Permissions
```bash
# Ensure write permissions
chmod 755 .
touch test_export.json  # Test file creation
```

---

## 🔍 Query Issues

### Problem: "Cypher queries return no results"

**Symptoms:**
- Neo4j Browser shows empty results
- Python queries return empty lists

**Solutions:**

#### 1. Check Data Existence
```cypher
-- In Neo4j Browser
MATCH (n) RETURN count(n) as total_nodes;
MATCH ()-[r]-() RETURN count(r) as total_relationships;
```

#### 2. Verify Label Names
```cypher
-- Check actual labels in database
MATCH (n) RETURN DISTINCT labels(n) as entity_types;
```

#### 3. Simple Test Query
```cypher
-- Start with simple query
MATCH (n) RETURN n LIMIT 5;
```

### Problem: "Performance is slow"

**Symptoms:**
- Queries take a long time
- Visualizations are slow to load

**Solutions:**

#### 1. Create Indexes
```cypher
-- Create indexes on frequently queried properties
CREATE INDEX entity_id IF NOT EXISTS FOR (n:Entity) ON (n.id);
CREATE INDEX entity_name IF NOT EXISTS FOR (n:Entity) ON (n.name);
```

#### 2. Use LIMIT Clauses
```cypher
-- Limit large queries
MATCH (n:Container) RETURN n LIMIT 100;
```

#### 3. Optimize Queries
```cypher
-- Use specific labels
MATCH (s:Server) WHERE s.id = 'server-01' RETURN s;
-- Instead of: MATCH (n) WHERE n.id = 'server-01' RETURN n;
```

---

## 🖥️ System-Specific Issues

### macOS Issues

#### Problem: "No module named '_bz2'" or similar

**Solutions:**
```bash
# Install missing system dependencies
xcode-select --install

# Install Python with proper modules
brew install python@3.11
```

#### Problem: "Permission denied" errors

**Solutions:**
```bash
# Fix permissions
sudo chown -R $(whoami) /usr/local/lib/python3.11/site-packages/

# Or use virtual environment
python -m venv venv
source venv/bin/activate
```

### Windows Issues

#### Problem: "Microsoft Visual C++ 14.0 is required"

**Solutions:**
```bash
# Install Microsoft C++ Build Tools
# Or use conda instead of pip
conda install neo4j-python-driver
```

#### Problem: "Path too long" errors

**Solutions:**
```bash
# Enable long path support
# Or use shorter directory names
cd C:\KGs  # Instead of very long path
```

### Linux Issues

#### Problem: "Unable to locate package" errors

**Solutions:**
```bash
# Update package manager
sudo apt update

# Install Python dev packages
sudo apt install python3-dev python3-pip

# Install system dependencies
sudo apt install build-essential
```

---

## 🧪 Testing and Debugging

### Enable Debug Logging

```python
import logging

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Now all operations will be logged
kg = Neo4jKnowledgeGraph()
```

### Test Database Connection

```python
def test_connection():
    try:
        kg = Neo4jKnowledgeGraph()
        result = kg.execute_query("RETURN 1 as test")
        print(f"✅ Connection successful: {result}")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

# Run test
test_connection()
```

### Verify Complete Setup

```python
def verify_setup():
    """Comprehensive setup verification"""
    checks = []
    
    # 1. Database connection
    try:
        kg = Neo4jKnowledgeGraph()
        kg.execute_query("RETURN 1")
        checks.append("✅ Database connection")
    except Exception as e:
        checks.append(f"❌ Database connection: {e}")
    
    # 2. Data generation
    try:
        from kg.data_generator import InfrastructureDataGenerator
        generator = InfrastructureDataGenerator(kg)
        checks.append("✅ Data generator import")
    except Exception as e:
        checks.append(f"❌ Data generator: {e}")
    
    # 3. Visualization
    try:
        from kg.visualization import GraphVisualizer
        viz = GraphVisualizer(kg)
        checks.append("✅ Visualization import")
    except Exception as e:
        checks.append(f"❌ Visualization: {e}")
    
    # 4. LLM interface
    try:
        from kg.llm_interface import KnowledgeGraphLLMInterface
        llm = KnowledgeGraphLLMInterface(kg)
        checks.append("✅ LLM interface import")
    except Exception as e:
        checks.append(f"❌ LLM interface: {e}")
    
    return checks

# Run verification
results = verify_setup()
for result in results:
    print(result)
```

---

## 📞 Getting Help

### Before Seeking Help

1. **Check the logs** - Enable debug logging and check for specific error messages
2. **Try minimal examples** - Use the simplest possible code to reproduce the issue
3. **Check versions** - Ensure you're using compatible versions of all dependencies
4. **Search existing issues** - Look through the documentation and any issue trackers

### Information to Include

When reporting issues, include:

- **Error messages** - Full stack traces
- **Environment details** - OS, Python version, package versions
- **Steps to reproduce** - Minimal code example
- **Expected vs actual behavior** - What you expected vs what happened
- **Configuration** - Any custom settings or modifications

### Common Commands for Debugging

```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(neo4j|streamlit|plotly|networkx)"

# Check Neo4j status
docker ps | grep neo4j
curl -I http://localhost:7474

# Test database connection
python -c "from kg.database import Neo4jKnowledgeGraph; kg = Neo4jKnowledgeGraph(); print('✅ Connection OK')"

# Check data count
python -c "from kg.database import Neo4jKnowledgeGraph; kg = Neo4jKnowledgeGraph(); print(kg.get_statistics())"
```

---

## 🔄 Reset and Clean Start

### Complete Reset

If you're experiencing multiple issues, try a complete reset:

```bash
# 1. Stop all services
docker stop neo4j-kg
pkill -f streamlit

# 2. Remove containers and volumes
docker rm neo4j-kg
docker volume prune

# 3. Clean Python environment
pip uninstall -y neo4j streamlit plotly pyvis networkx
pip install -r requirements.txt

# 4. Fresh Neo4j instance
docker run -d --name neo4j-kg -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password neo4j:latest

# 5. Wait for startup
sleep 30

# 6. Test setup
python -c "from kg.database import Neo4jKnowledgeGraph; kg = Neo4jKnowledgeGraph(); print('✅ Ready')"

# 7. Generate fresh data
python main.py
```

### Quick Health Check

```bash
# Run this script to check system health
python -c "
import sys
print(f'Python: {sys.version}')
try:
    import neo4j
    print(f'Neo4j driver: {neo4j.__version__}')
except ImportError:
    print('❌ Neo4j driver not installed')
    
try:
    import streamlit
    print(f'Streamlit: {streamlit.__version__}')
except ImportError:
    print('❌ Streamlit not installed')
    
try:
    from kg.database import Neo4jKnowledgeGraph
    kg = Neo4jKnowledgeGraph()
    stats = kg.get_statistics()
    print(f'Database: {stats[\"total_entities\"]} entities')
except Exception as e:
    print(f'❌ Database issue: {e}')
"
```

---

This troubleshooting guide should help you resolve most common issues. If you encounter problems not covered here, please check the other documentation files or seek help from the community. 