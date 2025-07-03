
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
