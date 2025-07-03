"""
Knowledge Graph Visualization Module
Supports multiple visualization backends: pyvis, plotly, networkx, streamlit
"""
import json
import os
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from pyvis.network import Network
from datetime import datetime

from .database import Neo4jKnowledgeGraph
from .models import EntityType, RelationshipType


class KnowledgeGraphVisualizer:
    """Comprehensive visualization for Neo4j Knowledge Graph"""
    
    def __init__(self, kg: Neo4jKnowledgeGraph):
        self.kg = kg
        self.entity_colors = {
            'NetworkSwitch': '#FF6B6B',      # Red
            'NetworkPort': '#4ECDC4',        # Teal
            'VLAN': '#45B7D1',               # Blue
            'Server': '#96CEB4',             # Green
            'VirtualMachine': '#FFEAA7',     # Yellow
            'KubernetesPod': '#DDA0DD',      # Plum
            'Container': '#98D8C8',          # Mint
        }
        
        self.relationship_colors = {
            'CONTAINS': '#FF6B6B',
            'HOSTS': '#4ECDC4',
            'RUNS_ON': '#45B7D1',
            'BELONGS_TO': '#96CEB4',
            'CONNECTED_TO': '#FFEAA7',
            'DEPLOYED_ON': '#DDA0DD',
            'PART_OF': '#98D8C8',
        }
    
    def get_graph_data(self) -> Dict[str, Any]:
        """Get complete graph data from Neo4j"""
        return self.kg.get_full_topology_graph()
    
    def create_networkx_graph(self, filter_entities: List[str] = None) -> nx.DiGraph:
        """Create a NetworkX graph from Neo4j data"""
        graph_data = self.get_graph_data()
        
        G = nx.DiGraph()
        
        # Add nodes (get_full_topology_graph returns 'nodes', not 'entities')
        for entity in graph_data.get('nodes', []):
            entity_type = entity.get('type', 'Unknown')
            if filter_entities and entity_type not in filter_entities:
                continue
                
            G.add_node(
                entity['id'],
                name=entity.get('name', ''),
                type=entity_type,
                color=self.entity_colors.get(entity_type, '#CCCCCC'),
                size=self._get_node_size(entity_type),
                **{k: v for k, v in entity.items() if k not in ['id', 'name', 'type']}
            )
        
        # Add edges (update to use correct relationship format)
        for relationship in graph_data.get('relationships', []):
            source = relationship.get('source_id')
            target = relationship.get('target_id')
            rel_type = relationship.get('relationship_type')
            
            if source and target and G.has_node(source) and G.has_node(target):
                G.add_edge(
                    source,
                    target,
                    type=rel_type,
                    color=self.relationship_colors.get(rel_type, '#CCCCCC'),
                    **relationship.get('properties', {})
                )
        
        return G
    
    def _get_node_size(self, entity_type: str) -> int:
        """Get node size based on entity type"""
        size_map = {
            'NetworkSwitch': 50,
            'NetworkPort': 20,
            'VLAN': 35,
            'Server': 45,
            'VirtualMachine': 30,
            'KubernetesPod': 25,
            'Container': 20,
        }
        return size_map.get(entity_type, 25)
    
    def create_pyvis_network(self, 
                           filter_entities: List[str] = None,
                           height: str = "600px",
                           width: str = "100%",
                           output_file: str = "network_topology.html") -> Network:
        """Create interactive network visualization using pyvis"""
        
        net = Network(height=height, width=width, bgcolor="#222222", font_color="white")
        net.set_options("""
        var options = {
          "nodes": {
            "font": {"size": 14},
            "scaling": {"min": 10, "max": 30}
          },
          "edges": {
            "color": {"inherit": false},
            "smooth": {"type": "continuous"},
            "arrows": {"to": {"enabled": true, "scaleFactor": 0.5}}
          },
          "physics": {
            "barnesHut": {
              "gravitationalConstant": -80000,
              "springConstant": 0.001,
              "springLength": 200
            },
            "minVelocity": 0.75
          }
        }
        """)
        
        G = self.create_networkx_graph(filter_entities)
        
        # Add nodes
        for node_id, node_data in G.nodes(data=True):
            net.add_node(
                node_id,
                label=node_data.get('name', node_id),
                color=node_data.get('color', '#CCCCCC'),
                size=node_data.get('size', 25),
                title=self._create_node_tooltip(node_data),
                group=node_data.get('type', 'Unknown')
            )
        
        # Add edges
        for source, target, edge_data in G.edges(data=True):
            net.add_edge(
                source,
                target,
                label=edge_data.get('type', ''),
                color=edge_data.get('color', '#CCCCCC'),
                title=self._create_edge_tooltip(edge_data)
            )
        
        try:
            net.save_graph(output_file)
            print(f"✅ Interactive network saved to: {output_file}")
        except Exception as e:
            print(f"⚠️  Warning: Could not save with save_graph, trying show: {e}")
            net.show(output_file)
            print(f"✅ Interactive network saved to: {output_file}")
        return net
    
    def _create_node_tooltip(self, node_data: Dict[str, Any]) -> str:
        """Create tooltip text for nodes"""
        tooltip = f"<b>{node_data.get('name', 'Unknown')}</b><br>"
        tooltip += f"Type: {node_data.get('type', 'Unknown')}<br>"
        
        # Add specific properties based on type
        if node_data.get('type') == 'Server':
            tooltip += f"Hostname: {node_data.get('hostname', 'N/A')}<br>"
            tooltip += f"CPU Cores: {node_data.get('cpu_cores', 'N/A')}<br>"
            tooltip += f"Memory: {node_data.get('memory_gb', 'N/A')} GB<br>"
        elif node_data.get('type') == 'VirtualMachine':
            tooltip += f"Hostname: {node_data.get('hostname', 'N/A')}<br>"
            tooltip += f"OS: {node_data.get('os', 'N/A')}<br>"
        elif node_data.get('type') == 'KubernetesPod':
            tooltip += f"Namespace: {node_data.get('namespace', 'N/A')}<br>"
            tooltip += f"Phase: {node_data.get('phase', 'N/A')}<br>"
        elif node_data.get('type') == 'Container':
            tooltip += f"Image: {node_data.get('image', 'N/A')}<br>"
            tooltip += f"Status: {node_data.get('status', 'N/A')}<br>"
        
        return tooltip
    
    def _create_edge_tooltip(self, edge_data: Dict[str, Any]) -> str:
        """Create tooltip text for edges"""
        tooltip = f"<b>{edge_data.get('type', 'Unknown')}</b><br>"
        for key, value in edge_data.items():
            if key not in ['type', 'color']:
                tooltip += f"{key}: {value}<br>"
        return tooltip
    
    def create_plotly_network(self, 
                            filter_entities: List[str] = None,
                            layout_algorithm: str = "spring") -> go.Figure:
        """Create interactive network visualization using plotly"""
        
        G = self.create_networkx_graph(filter_entities)
        
        # Calculate layout
        if layout_algorithm == "spring":
            pos = nx.spring_layout(G, k=3, iterations=50)
        elif layout_algorithm == "circular":
            pos = nx.circular_layout(G)
        elif layout_algorithm == "kamada_kawai":
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.spring_layout(G)
        
        # Create edge traces
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Create node traces by type
        node_traces = []
        for node_type, color in self.entity_colors.items():
            nodes = [node for node, data in G.nodes(data=True) if data.get('type') == node_type]
            if not nodes:
                continue
                
            node_x = []
            node_y = []
            node_text = []
            node_info = []
            
            for node in nodes:
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_text.append(G.nodes[node].get('name', node))
                node_info.append(f"{node_type}: {G.nodes[node].get('name', node)}")
            
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                marker=dict(
                    size=20,
                    color=color,
                    line=dict(width=2, color='white')
                ),
                text=node_text,
                textposition="middle center",
                name=node_type,
                hoverinfo='text',
                hovertext=node_info
            )
            node_traces.append(node_trace)
        
        # Create figure
        fig = go.Figure(data=[edge_trace] + node_traces)
        
        fig.update_layout(
            title=dict(text="Network Infrastructure Topology", font=dict(size=16)),
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[
                dict(
                    text="Interactive Network Topology - Click and drag to explore",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002,
                    xanchor="left", yanchor="bottom",
                    font=dict(color="#888", size=12)
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_hierarchy_view(self) -> go.Figure:
        """Create hierarchical view of the infrastructure"""
        
        # Get statistics
        stats = self.kg.get_statistics()
        entity_counts = stats.get('entity_counts', {})
        
        # Create bar chart
        fig = go.Figure()
        
        entity_types = list(entity_counts.keys())
        counts = list(entity_counts.values())
        colors = [self.entity_colors.get(et, '#CCCCCC') for et in entity_types]
        
        fig.add_trace(go.Bar(
            x=entity_types,
            y=counts,
            marker_color=colors,
            text=counts,
            textposition='auto',
        ))
        
        fig.update_layout(
            title="Infrastructure Entity Distribution",
            xaxis_title="Entity Type",
            yaxis_title="Count",
            showlegend=False
        )
        
        return fig
    
    def create_static_graph(self, 
                          filter_entities: List[str] = None,
                          output_file: str = "topology_static.png",
                          figsize: Tuple[int, int] = (15, 10)) -> None:
        """Create static network visualization using matplotlib"""
        
        G = self.create_networkx_graph(filter_entities)
        
        plt.figure(figsize=figsize)
        
        # Calculate layout
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color='#CCCCCC', alpha=0.6, width=1)
        
        # Draw nodes by type
        for entity_type, color in self.entity_colors.items():
            nodes = [node for node, data in G.nodes(data=True) if data.get('type') == entity_type]
            if nodes:
                nx.draw_networkx_nodes(
                    G, pos, nodelist=nodes,
                    node_color=color,
                    node_size=[G.nodes[node].get('size', 25) * 10 for node in nodes],
                    alpha=0.8,
                    label=entity_type
                )
        
        # Draw labels
        labels = {node: data.get('name', node)[:15] for node, data in G.nodes(data=True)}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        plt.title("Network Infrastructure Topology", size=16)
        plt.legend(scatterpoints=1, loc='upper left', bbox_to_anchor=(1, 1))
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Static graph saved to: {output_file}")
    
    def generate_all_visualizations(self, output_dir: str = "visualizations") -> Dict[str, str]:
        """Generate all types of visualizations"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        outputs = {}
        
        # 1. Interactive HTML network
        html_file = os.path.join(output_dir, "interactive_network.html")
        self.create_pyvis_network(output_file=html_file)
        outputs['interactive_html'] = html_file
        
        # 2. Static PNG
        png_file = os.path.join(output_dir, "topology_static.png")
        self.create_static_graph(output_file=png_file)
        outputs['static_png'] = png_file
        
        # 3. Plotly HTML
        plotly_fig = self.create_plotly_network()
        plotly_file = os.path.join(output_dir, "plotly_network.html")
        plotly_fig.write_html(plotly_file)
        outputs['plotly_html'] = plotly_file
        
        # 4. Hierarchy chart
        hierarchy_fig = self.create_hierarchy_view()
        hierarchy_file = os.path.join(output_dir, "hierarchy_chart.html")
        hierarchy_fig.write_html(hierarchy_file)
        outputs['hierarchy_html'] = hierarchy_file
        
        # 5. Filtered views
        filters = {
            'network_layer': ['NetworkSwitch', 'NetworkPort', 'VLAN'],
            'compute_layer': ['Server', 'VirtualMachine'],
            'container_layer': ['KubernetesPod', 'Container']
        }
        
        for layer_name, entity_types in filters.items():
            filtered_file = os.path.join(output_dir, f"filtered_{layer_name}.html")
            self.create_pyvis_network(filter_entities=entity_types, output_file=filtered_file)
            outputs[f'filtered_{layer_name}'] = filtered_file
        
        return outputs


def create_streamlit_app():
    """Create a Streamlit app file for the dashboard"""
    
    streamlit_code = '''
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(__file__))

from kg.visualization import KnowledgeGraphVisualizer
from kg.database import Neo4jKnowledgeGraph

st.set_page_config(
    page_title="Network Infrastructure Topology",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Network Infrastructure Knowledge Graph")
st.markdown("Interactive visualization of your network topology")

# Initialize visualizer
@st.cache_resource
def get_visualizer():
    try:
        kg = Neo4jKnowledgeGraph()
        return KnowledgeGraphVisualizer(kg)
    except Exception as e:
        st.error(f"Error connecting to Neo4j: {e}")
        return None

visualizer = get_visualizer()

if visualizer:
    # Sidebar controls
    st.sidebar.header("Visualization Controls")
    
    # Entity filter
    all_entities = list(visualizer.entity_colors.keys())
    selected_entities = st.sidebar.multiselect(
        "Filter Entity Types",
        all_entities,
        default=all_entities
    )
    
    # Layout algorithm
    layout_algo = st.sidebar.selectbox(
        "Layout Algorithm",
        ["spring", "circular", "kamada_kawai"]
    )
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Interactive Network Topology")
        
        # Create and display plotly network
        fig = visualizer.create_plotly_network(
            filter_entities=selected_entities if selected_entities else None,
            layout_algorithm=layout_algo
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Infrastructure Overview")
        
        # Display statistics
        stats = visualizer.kg.get_statistics()
        st.metric("Total Entities", stats.get('total_entities', 0))
        st.metric("Total Relationships", stats.get('total_relationships', 0))
        
        # Entity breakdown
        st.subheader("Entity Distribution")
        entity_counts = stats.get('entity_counts', {})
        for entity_type, count in entity_counts.items():
            st.metric(entity_type, count)
    
    # Hierarchy view
    st.subheader("Entity Distribution Chart")
    hierarchy_fig = visualizer.create_hierarchy_view()
    st.plotly_chart(hierarchy_fig, use_container_width=True)
    
    # Export options
    st.subheader("Export Options")
    if st.button("Generate All Visualizations"):
        with st.spinner("Generating visualizations..."):
            outputs = visualizer.generate_all_visualizations()
            st.success(f"Generated {len(outputs)} visualizations!")
            for name, path in outputs.items():
                st.text(f"✅ {name}: {path}")
else:
    st.error("Could not connect to Neo4j database. Please ensure it's running.")
'''
    
    with open("streamlit_app.py", "w") as f:
        f.write(streamlit_code)
    
    print("✅ Streamlit app created: streamlit_app.py")


if __name__ == "__main__":
    # Example usage
    kg = Neo4jKnowledgeGraph()
    visualizer = KnowledgeGraphVisualizer(kg)
    
    # Generate all visualizations
    outputs = visualizer.generate_all_visualizations()
    
    print("📊 Generated visualizations:")
    for name, path in outputs.items():
        print(f"  ✅ {name}: {path}")
    
    kg.close() 