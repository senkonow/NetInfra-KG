# 🎨 Knowledge Graph Visualization Guide

## Overview

This guide explains how to visualize your Neo4j network infrastructure knowledge graph using multiple visualization approaches. The system provides interactive HTML networks, static images, web dashboards, and integration with Grafana.

## 📊 Available Visualizations

### 1. Interactive HTML Networks (Pyvis)
**Files**: `interactive_network.html`, `demo_interactive.html`

**Features**:
- Fully interactive network graphs
- Click and drag nodes
- Zoom and pan
- Hover tooltips with entity details
- Physics-based layout simulation
- Color-coded by entity type

**Usage**:
```bash
# Generate interactive network
python demo_visualizations.py
# Then open: visualizations/interactive_network.html
```

### 2. Static PNG Images (Matplotlib)
**Files**: `topology_static.png`, `demo_static.png`

**Features**:
- High-resolution static images
- Color-coded entities
- Suitable for presentations and reports
- Customizable layouts

**Usage**:
```bash
# View static image
open visualizations/topology_static.png
```

### 3. Hierarchy Charts (Plotly)
**Files**: `hierarchy_chart.html`, `demo_hierarchy.html`

**Features**:
- Bar charts showing entity distribution
- Interactive hover information
- Color-coded by entity type
- Good for understanding infrastructure composition

### 4. Filtered Views
**Files**: 
- `filtered_network_infrastructure.html` (Switches, Ports, VLANs)
- `filtered_compute_resources.html` (Servers, VMs)
- `filtered_container_platform.html` (Pods, Containers)

**Features**:
- Focus on specific infrastructure layers
- Reduced complexity for targeted analysis
- Interactive exploration of subsystems

### 5. Streamlit Web Dashboard
**File**: `streamlit_app.py`

**Features**:
- Real-time interactive web interface
- Multiple visualization types in one place
- Filter controls for entity types
- Layout algorithm selection
- Statistics overview

**Usage**:
```bash
# Run dashboard (available at http://localhost:8501)
streamlit run streamlit_app.py
```

### 6. Grafana Integration
**File**: `visualizations/grafana_dashboard.json`

**Features**:
- Professional monitoring dashboard
- Real-time metrics
- Entity counts and distributions
- Resource utilization tracking
- Alert capabilities

## 🚀 Quick Start

### 1. Generate All Visualizations
```bash
python demo_visualizations.py
```

### 2. Open Interactive Visualizations
```bash
# Main network topology
open visualizations/interactive_network.html

# Filtered views
open visualizations/filtered_network_infrastructure.html
open visualizations/filtered_compute_resources.html
open visualizations/filtered_container_platform.html

# Charts
open visualizations/hierarchy_chart.html
```

### 3. Run Web Dashboard
```bash
streamlit run streamlit_app.py
# Then visit: http://localhost:8501
```

### 4. View Static Images
```bash
open visualizations/topology_static.png
```

## 🎯 Use Cases by Visualization Type

### Interactive HTML Networks
- **Best for**: Exploring relationships, understanding topology
- **Use when**: You need to trace paths between entities
- **Features**: Click nodes to see connections, drag to reorganize

### Static Images
- **Best for**: Documentation, presentations, reports
- **Use when**: You need printable or embedded images
- **Features**: High resolution, consistent layout

### Hierarchy Charts
- **Best for**: Understanding infrastructure composition
- **Use when**: You want to see entity distributions
- **Features**: Clear breakdown of entity types and counts

### Filtered Views
- **Best for**: Layer-specific analysis
- **Use when**: You want to focus on specific infrastructure parts
- **Examples**:
  - Network layer: Switches, ports, VLANs
  - Compute layer: Servers, VMs
  - Container layer: Pods, containers

### Streamlit Dashboard
- **Best for**: Interactive exploration and analysis
- **Use when**: You need real-time filtering and multiple views
- **Features**: All visualizations in one interface

### Grafana Integration
- **Best for**: Monitoring and alerting
- **Use when**: You need operational dashboards
- **Features**: Real-time metrics, historical data, alerts

## 🔧 Customization

### Modify Colors
Edit `kg/visualization.py`:
```python
self.entity_colors = {
    'NetworkSwitch': '#FF6B6B',    # Red
    'Server': '#96CEB4',           # Green
    # Add more colors...
}
```

### Filter Entity Types
```python
# Create filtered visualization
visualizer.create_pyvis_network(
    filter_entities=['Server', 'VirtualMachine'],
    output_file='servers_only.html'
)
```

### Change Layout Algorithms
```python
# For Plotly networks
fig = visualizer.create_plotly_network(layout_algorithm='circular')
# Options: 'spring', 'circular', 'kamada_kawai'
```

### Adjust Node Sizes
Edit `_get_node_size()` method in `kg/visualization.py`:
```python
size_map = {
    'NetworkSwitch': 60,    # Larger switches
    'Container': 15,        # Smaller containers
}
```

## 📈 Grafana Setup

### 1. Install Grafana
```bash
# Using Docker
docker run -d -p 3000:3000 grafana/grafana-enterprise

# Or install directly
# See: https://grafana.com/docs/grafana/latest/installation/
```

### 2. Add Neo4j Data Source
1. Open Grafana at http://localhost:3000
2. Go to Configuration > Data Sources
3. Add Neo4j data source
4. Configure connection:
   - URL: `bolt://localhost:7687`
   - Username: `neo4j`
   - Password: `password`

### 3. Import Dashboard
1. Go to Dashboards > Import
2. Upload `visualizations/grafana_dashboard.json`
3. Configure data source mapping

### 4. Example Queries
```cypher
# Entity count by type
MATCH (n)
RETURN labels(n)[1] as entity_type, count(n) as count
ORDER BY count DESC

# Resource utilization
MATCH (s:Server)
RETURN sum(s.cpu_cores) as total_cores, sum(s.memory_gb) as total_memory

# Container distribution
MATCH (p:KubernetesPod)
RETURN p.namespace as namespace, count(p) as pod_count
ORDER BY pod_count DESC
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Scipy Missing Error
```bash
# Solution
uv pip install scipy
```

#### 2. Empty Visualizations
- Check if Neo4j is running: http://localhost:7474
- Verify data exists: Run `python main.py` first
- Check database connection in code

#### 3. Streamlit Port Conflicts
```bash
# Use different port
streamlit run streamlit_app.py --server.port 8502
```

#### 4. Large Graph Performance
- Use filtered views for better performance
- Reduce node count with entity filters
- Consider static images for very large graphs

### Performance Tips

1. **For Large Graphs (1000+ nodes)**:
   - Use filtered views
   - Consider static visualizations
   - Implement pagination in Streamlit

2. **For Real-time Updates**:
   - Use Grafana for monitoring
   - Implement data refresh in Streamlit
   - Consider websocket updates

3. **For Presentation**:
   - Use static PNG images
   - Create filtered views for clarity
   - Export specific subgraphs

## 📚 Additional Resources

### Documentation
- [Pyvis Documentation](https://pyvis.readthedocs.io/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Grafana Documentation](https://grafana.com/docs/)

### Examples
- Check `demo_visualizations.py` for complete examples
- Explore `kg/visualization.py` for implementation details
- See generated HTML files for interactive features

### Extensions
- Add more entity types in `models.py`
- Create custom layouts in `visualization.py`
- Implement new chart types with Plotly
- Add real-time data updates

## 🎉 Summary

You now have multiple ways to visualize your network infrastructure knowledge graph:

1. **Interactive HTML** - For exploration and analysis
2. **Static Images** - For documentation and presentations  
3. **Web Dashboard** - For real-time interaction
4. **Grafana** - For monitoring and alerting
5. **Filtered Views** - For focused analysis

Each visualization type serves different purposes and can be customized to your specific needs. Start with the interactive HTML files to explore your topology, then use the Streamlit dashboard for ongoing analysis! 