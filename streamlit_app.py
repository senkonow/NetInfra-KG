# =============================================================================
# STREAMLIT_APP.PY - INTERACTIVE WEB DASHBOARD FOR NETWORK INFRASTRUCTURE KNOWLEDGE GRAPH
# =============================================================================
# This file creates a web-based dashboard for exploring our network infrastructure knowledge graph
# Think of it as creating a "website" that people can visit to interact with our data
#
# WHAT IS STREAMLIT?
# Streamlit is a Python library that makes it easy to create interactive web applications
# Instead of learning HTML, CSS, and JavaScript, you can build web apps using just Python
# It's like having a "website builder" that understands Python code
#
# WHAT IS A WEB DASHBOARD?
# A web dashboard is like a "control panel" that you access through a web browser
# It displays information and provides interactive controls to explore the data
# Think of it like the dashboard in your car - it shows you important information
# and has controls you can use
#
# WHAT DOES THIS DASHBOARD DO?
# 1. Shows interactive network topology visualizations
# 2. Provides filtering controls to focus on specific parts of the network
# 3. Displays statistics about the infrastructure
# 4. Allows users to export visualizations
# 5. Updates in real-time as users interact with the controls
#
# HOW TO RUN THIS DASHBOARD:
# streamlit run streamlit_app.py
# Then open your web browser to http://localhost:8501

# IMPORT STATEMENTS - Getting tools we need from other Python libraries
# =============================================================================

# streamlit: The main library for creating web applications
# We import it as 'st' for convenience (shorter to type)
import streamlit as st

# sys and os: For working with the file system and Python paths
# We need these to make sure Python can find our custom modules
import sys
import os

# Add the current directory to Python's path so it can find our 'kg' package
# This is like telling Python "look in this folder for our custom code"
sys.path.append(os.path.dirname(__file__))

# Import our custom visualization and database classes
# These are the tools we built for working with the knowledge graph
from kg.visualization import KnowledgeGraphVisualizer
from kg.database import Neo4jKnowledgeGraph


# PAGE CONFIGURATION - Setting up how the web page looks and behaves
# =============================================================================

# Configure the Streamlit page settings
# This is like setting up the "theme" and layout of our web page
st.set_page_config(
    page_title="Network Infrastructure Topology",  # Title shown in browser tab
    page_icon="🌐",                                 # Icon shown in browser tab (globe emoji)
    layout="wide"                                   # Use full width of the browser window
)

# PAGE HEADER - The title and description users see at the top
# =============================================================================

# Create the main title of our dashboard
# st.title() creates a large heading at the top of the page
st.title("🌐 Network Infrastructure Knowledge Graph")

# Add a subtitle/description below the main title
# st.markdown() allows us to format text (like bold, italic, etc.)
st.markdown("Interactive visualization of your network topology")


# INITIALIZATION FUNCTIONS - Setting up the dashboard components
# =============================================================================

@st.cache_resource
def get_visualizer():
    """
    Initialize the knowledge graph visualizer
    
    WHAT IS @st.cache_resource?
    This is a "decorator" that tells Streamlit to cache (remember) the result
    Think of it like "remembering" the database connection so we don't have to
    create a new one every time the user interacts with the page
    
    WHY DO WE NEED CACHING?
    Creating database connections is slow and expensive
    By caching, we create the connection once and reuse it
    This makes the dashboard much faster and more responsive
    
    WHAT DOES THIS FUNCTION DO?
    1. Connects to the Neo4j database
    2. Creates a visualizer object that can generate graphs
    3. Returns the visualizer for use throughout the dashboard
    4. If connection fails, returns None and shows an error message
    """
    try:
        # WHAT IS TRY/EXCEPT?
        # This is error handling - we try to do something, and if it fails,
        # we have a backup plan instead of crashing the entire application
        
        # Create a connection to the Neo4j database
        kg = Neo4jKnowledgeGraph()
        
        # Create a visualizer that can generate graphs from the database
        return KnowledgeGraphVisualizer(kg)
        
    except Exception as e:
        # If anything goes wrong (database not running, wrong password, etc.)
        # Display a user-friendly error message on the web page
        st.error(f"Error connecting to Neo4j: {e}")
        return None


# MAIN DASHBOARD INITIALIZATION
# =============================================================================

# Call our initialization function to set up the visualizer
# This creates the database connection and visualizer that we'll use throughout the dashboard
visualizer = get_visualizer()

# Check if initialization was successful
if visualizer:
    # If we successfully connected to the database, show the main dashboard
    
    # SIDEBAR CONTROLS - Interactive controls on the left side of the page
    # -------------------------------------------------------------------------
    
    # Create a sidebar header
    # The sidebar is like a "control panel" that stays visible while users explore
    st.sidebar.header("Visualization Controls")
    
    # ENTITY TYPE FILTER - Let users choose which types of entities to show
    # -------------------------------------------------------------------------
    
    # Get all available entity types from the visualizer
    # entity_colors is a dictionary that maps entity types to display colors
    all_entities = list(visualizer.entity_colors.keys())
    
    # Create a multi-select widget for filtering entity types
    # Users can check/uncheck different entity types to show/hide them
    selected_entities = st.sidebar.multiselect(
        "Filter Entity Types",           # Label shown to users
        all_entities,                   # List of options to choose from
        default=all_entities            # By default, show all entity types
    )
    
    # LAYOUT ALGORITHM SELECTOR - Let users choose how the graph is arranged
    # -------------------------------------------------------------------------
    
    # Create a dropdown menu for selecting the layout algorithm
    # Different algorithms arrange the nodes in different patterns
    layout_algo = st.sidebar.selectbox(
        "Layout Algorithm",             # Label shown to users
        ["spring", "circular", "kamada_kawai"]  # Available layout options
    )
    
    # WHAT ARE LAYOUT ALGORITHMS?
    # - spring: Nodes are arranged like they're connected by springs (natural looking)
    # - circular: Nodes are arranged in a circle
    # - kamada_kawai: A sophisticated algorithm that minimizes edge crossings
    
    # MAIN CONTENT AREA - The primary visualization and information display
    # -------------------------------------------------------------------------
    
    # Create two columns for the main content
    # col1 will be twice as wide as col2 (ratio 2:1)
    col1, col2 = st.columns([2, 1])
    
    # LEFT COLUMN - Interactive network visualization
    # -------------------------------------------------------------------------
    with col1:
        # Create a subheader for this section
        st.subheader("Interactive Network Topology")
        
        # Create the main network visualization
        # This generates an interactive graph that users can zoom, pan, and explore
        fig = visualizer.create_plotly_network(
            # Apply entity filter if user has made selections
            filter_entities=selected_entities if selected_entities else None,
            layout_algorithm=layout_algo  # Use the selected layout algorithm
        )
        
        # Display the interactive graph
        # use_container_width=True makes the graph fill the available space
        st.plotly_chart(fig, use_container_width=True)
    
    # RIGHT COLUMN - Statistics and information display
    # -------------------------------------------------------------------------
    with col2:
        # Create a subheader for this section
        st.subheader("Infrastructure Overview")
        
        # STATISTICS DISPLAY - Show key metrics about the infrastructure
        # -------------------------------------------------------------------------
        
        # Get current statistics from the database
        stats = visualizer.kg.get_statistics()
        
        # Display key metrics using Streamlit's metric widget
        # st.metric() creates a nice-looking number display with a label
        st.metric("Total Entities", stats.get('total_entities', 0))
        st.metric("Total Relationships", stats.get('total_relationships', 0))
        
        # ENTITY BREAKDOWN - Show count of each entity type
        # -------------------------------------------------------------------------
        
        # Create another subheader for the entity breakdown
        st.subheader("Entity Distribution")
        
        # Get the count of each entity type
        entity_counts = stats.get('entity_counts', {})
        
        # Display each entity type count as a metric
        for entity_type, count in entity_counts.items():
            st.metric(entity_type, count)
    
    # HIERARCHY VISUALIZATION - Show entity distribution as a chart
    # -------------------------------------------------------------------------
    
    # Create a subheader for this section
    st.subheader("Entity Distribution Chart")
    
    # Generate a bar chart showing the distribution of entity types
    hierarchy_fig = visualizer.create_hierarchy_view()
    
    # Display the chart
    st.plotly_chart(hierarchy_fig, use_container_width=True)
    
    # EXPORT OPTIONS - Allow users to generate and download visualizations
    # -------------------------------------------------------------------------
    
    # Create a subheader for this section
    st.subheader("Export Options")
    
    # Create a button that triggers visualization generation
    # st.button() returns True when the button is clicked
    if st.button("Generate All Visualizations"):
        # WHAT IS st.spinner()?
        # This shows a loading indicator while the code inside is running
        # It's like showing users a "please wait" message
        
        with st.spinner("Generating visualizations..."):
            # Call the visualizer to generate all visualization types
            # This creates HTML files, PNG images, and other formats
            outputs = visualizer.generate_all_visualizations()
            
            # Show a success message when generation is complete
            st.success(f"Generated {len(outputs)} visualizations!")
            
            # List all the generated files for the user
            for name, path in outputs.items():
                st.text(f"✅ {name}: {path}")

else:
    # ERROR STATE - Show this if we couldn't connect to the database
    # -------------------------------------------------------------------------
    
    # If the visualizer initialization failed, show an error message
    # This happens when Neo4j is not running or connection settings are wrong
    st.error("Could not connect to Neo4j database. Please ensure it's running.")
    
    # HELPFUL TROUBLESHOOTING INFORMATION
    # -------------------------------------------------------------------------
    
    # Provide users with helpful information to resolve the connection issue
    st.markdown("""
    **Troubleshooting Steps:**
    
    1. **Check if Neo4j is running:**
       - If using Docker: `docker ps` should show a Neo4j container
       - If using local installation: Check if Neo4j service is started
    
    2. **Verify connection settings:**
       - Default URL: `bolt://localhost:7687`
       - Default username: `neo4j`
       - Default password: `password`
    
    3. **Check environment variables:**
       - `NEO4J_URI`: Database connection URL
       - `NEO4J_USERNAME`: Database username
       - `NEO4J_PASSWORD`: Database password
    
    4. **Test connection manually:**
       - Run `python main.py` to test the connection
       - Check the Neo4j browser at `http://localhost:7474`
    """)

# APPLICATION FOOTER - Additional information and instructions
# =============================================================================

# Add some spacing
st.markdown("---")  # Creates a horizontal line

# Provide instructions for users
st.markdown("""
**How to Use This Dashboard:**

1. **Filter Entity Types:** Use the sidebar to show/hide different types of network equipment
2. **Change Layout:** Try different layout algorithms to see the network from different perspectives  
3. **Explore Interactively:** Click and drag to zoom and pan around the network visualization
4. **View Statistics:** Check the right panel for infrastructure metrics and entity counts
5. **Export Visualizations:** Click the export button to generate downloadable visualizations

**About This System:**
This dashboard visualizes a Neo4j knowledge graph containing network infrastructure topology data. 
The graph shows relationships between switches, servers, virtual machines, Kubernetes pods, and containers.
""")

# PERFORMANCE AND TECHNICAL NOTES
# =============================================================================

# Add technical information for advanced users
with st.expander("Technical Information"):
    st.markdown("""
    **Technology Stack:**
    - **Frontend:** Streamlit (Python web framework)
    - **Database:** Neo4j graph database
    - **Visualizations:** Plotly (interactive charts) and Pyvis (network graphs)
    - **Data Processing:** NetworkX (graph algorithms) and Pandas (data manipulation)
    
    **Performance Notes:**
    - Visualizations are cached for better performance
    - Large networks (>1000 nodes) may take longer to render
    - Interactive features work best with modern web browsers
    
    **Data Sources:**
    - Entity data is stored in Neo4j as nodes with properties
    - Relationships define how entities connect to each other
    - Sample data includes realistic network infrastructure hierarchies
    """)

# DEVELOPMENT AND CUSTOMIZATION INFORMATION
# =============================================================================

# Add information for developers who want to extend the system
with st.expander("Development Information"):
    st.markdown("""
    **Customizing This Dashboard:**
    
    1. **Adding New Visualizations:**
       - Modify `kg/visualization.py` to add new chart types
       - Update this file to include new visualization controls
    
    2. **Changing the Layout:**
       - Modify the `st.columns()` configuration to adjust column widths
       - Add new sections using `st.subheader()` and content blocks
    
    3. **Adding New Filters:**
       - Create new sidebar controls using `st.sidebar.selectbox()` or `st.sidebar.multiselect()`
       - Pass filter parameters to the visualization functions
    
    4. **Performance Optimization:**
       - Use `@st.cache_data` for expensive data processing
       - Use `@st.cache_resource` for database connections and heavy objects
       - Consider pagination for very large datasets
    
    **File Structure:**
    ```
    streamlit_app.py          # This dashboard file
    kg/
    ├── database.py          # Neo4j connection and queries
    ├── visualization.py     # Chart and graph generation
    ├── models.py           # Data structure definitions
    └── llm_interface.py    # Natural language query processing
    ```
    """)
