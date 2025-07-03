#!/usr/bin/env python3
"""
Demo script for Knowledge Graph Visualization
Demonstrates all visualization capabilities
"""
import os
import time
from kg.database import Neo4jKnowledgeGraph
from kg.visualization import KnowledgeGraphVisualizer, create_streamlit_app


def main():
    """Main demo function"""
    print("🎨 Knowledge Graph Visualization Demo")
    print("=" * 50)
    
    # Initialize components
    try:
        kg = Neo4jKnowledgeGraph()
        visualizer = KnowledgeGraphVisualizer(kg)
        print("✅ Connected to Neo4j successfully")
    except Exception as e:
        print(f"❌ Failed to connect to Neo4j: {e}")
        print("Please ensure Neo4j is running and accessible.")
        return
    
    # Check if data exists
    stats = kg.get_statistics()
    if stats['total_entities'] == 0:
        print("⚠️  No data found in the knowledge graph!")
        print("Please run 'python main.py' first to populate the database.")
        return
    
    print(f"📊 Found {stats['total_entities']} entities and {stats['total_relationships']} relationships")
    
    # Create output directory
    output_dir = "visualizations"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Generate all visualizations
    print("\n1. 🎯 Generating All Visualizations...")
    print("-" * 40)
    
    outputs = {}
    
    # Generate each visualization individually to handle errors gracefully
    print("Generating interactive HTML network...")
    try:
        html_file = os.path.join(output_dir, "interactive_network.html")
        visualizer.create_pyvis_network(output_file=html_file)
        outputs['interactive_html'] = html_file
    except Exception as e:
        print(f"❌ Error creating interactive HTML: {e}")
    
    print("Generating static PNG image...")
    try:
        png_file = os.path.join(output_dir, "topology_static.png")
        visualizer.create_static_graph(output_file=png_file)
        outputs['static_png'] = png_file
    except Exception as e:
        print(f"❌ Error creating static PNG: {e}")
    
    print("Generating Plotly network...")
    try:
        plotly_fig = visualizer.create_plotly_network()
        plotly_file = os.path.join(output_dir, "plotly_network.html")
        plotly_fig.write_html(plotly_file)
        outputs['plotly_html'] = plotly_file
    except Exception as e:
        print(f"❌ Error creating Plotly network: {e}")
    
    print("Generating hierarchy chart...")
    try:
        hierarchy_fig = visualizer.create_hierarchy_view()
        hierarchy_file = os.path.join(output_dir, "hierarchy_chart.html")
        hierarchy_fig.write_html(hierarchy_file)
        outputs['hierarchy_html'] = hierarchy_file
    except Exception as e:
        print(f"❌ Error creating hierarchy chart: {e}")
    
    print(f"✅ Successfully generated {len(outputs)} visualizations:")
    
    # 2. Create individual visualizations with demos
    print("\n2. 🖼️  Creating Individual Visualizations...")
    print("-" * 40)
    
    # Interactive HTML Network
    print("Creating interactive HTML network...")
    try:
        interactive_file = os.path.join(output_dir, "demo_interactive.html")
        visualizer.create_pyvis_network(output_file=interactive_file)
        print(f"✅ Interactive HTML: {interactive_file}")
    except Exception as e:
        print(f"❌ Error creating interactive network: {e}")
    
    # Static PNG
    print("Creating static PNG image...")
    try:
        static_file = os.path.join(output_dir, "demo_static.png")
        visualizer.create_static_graph(output_file=static_file)
        print(f"✅ Static PNG: {static_file}")
    except Exception as e:
        print(f"❌ Error creating static graph: {e}")
    
    # Plotly Network
    print("Creating Plotly interactive network...")
    try:
        plotly_fig = visualizer.create_plotly_network()
        plotly_file = os.path.join(output_dir, "demo_plotly.html")
        plotly_fig.write_html(plotly_file)
        print(f"✅ Plotly Network: {plotly_file}")
    except Exception as e:
        print(f"❌ Error creating Plotly network: {e}")
    
    # Hierarchy Chart
    print("Creating hierarchy chart...")
    try:
        hierarchy_fig = visualizer.create_hierarchy_view()
        hierarchy_file = os.path.join(output_dir, "demo_hierarchy.html")
        hierarchy_fig.write_html(hierarchy_file)
        print(f"✅ Hierarchy Chart: {hierarchy_file}")
    except Exception as e:
        print(f"❌ Error creating hierarchy chart: {e}")
    
    # 3. Create filtered visualizations
    print("\n3. 🔍 Creating Filtered Visualizations...")
    print("-" * 40)
    
    filters = {
        'Network Infrastructure': ['NetworkSwitch', 'NetworkPort', 'VLAN'],
        'Compute Resources': ['Server', 'VirtualMachine'],
        'Container Platform': ['KubernetesPod', 'Container']
    }
    
    for filter_name, entity_types in filters.items():
        try:
            filter_file = os.path.join(output_dir, f"filtered_{filter_name.lower().replace(' ', '_')}.html")
            visualizer.create_pyvis_network(
                filter_entities=entity_types,
                output_file=filter_file
            )
            print(f"✅ {filter_name}: {filter_file}")
        except Exception as e:
            print(f"❌ Error creating {filter_name} filter: {e}")
    
    # 4. Create Streamlit app
    print("\n4. 🚀 Creating Streamlit Dashboard...")
    print("-" * 40)
    
    try:
        create_streamlit_app()
        print("✅ Streamlit app created: streamlit_app.py")
        print("   Run with: streamlit run streamlit_app.py")
    except Exception as e:
        print(f"❌ Error creating Streamlit app: {e}")
    
    # 5. Create Grafana dashboard config
    print("\n5. 📊 Creating Grafana Dashboard Config...")
    print("-" * 40)
    
    try:
        create_grafana_config(output_dir)
        print("✅ Grafana config created")
    except Exception as e:
        print(f"❌ Error creating Grafana config: {e}")
    
    # Summary and next steps
    print("\n" + "=" * 50)
    print("🎉 VISUALIZATION DEMO COMPLETE!")
    print("=" * 50)
    
    print("\n📂 Generated Files:")
    print(f"   📁 All visualizations: {output_dir}/")
    print("   📄 Streamlit app: streamlit_app.py")
    print("   📄 Grafana config: grafana_dashboard.json")
    
    print("\n🚀 Next Steps:")
    print("   1. Open interactive visualizations in your browser:")
    print(f"      - {os.path.join(output_dir, 'interactive_network.html')}")
    print(f"      - {os.path.join(output_dir, 'plotly_network.html')}")
    
    print("\n   2. Run Streamlit dashboard:")
    print("      streamlit run streamlit_app.py")
    
    print("\n   3. View static images:")
    print(f"      open {os.path.join(output_dir, 'topology_static.png')}")
    
    print("\n   4. Import Grafana dashboard:")
    print("      - Import grafana_dashboard.json in Grafana")
    print("      - Configure Neo4j data source")
    
    print("\n   5. Explore filtered views:")
    for filter_name in filters.keys():
        filename = f"filtered_{filter_name.lower().replace(' ', '_')}.html"
        print(f"      - {os.path.join(output_dir, filename)}")
    
    kg.close()


def create_grafana_config(output_dir: str):
    """Create Grafana dashboard configuration"""
    
    grafana_config = {
        "dashboard": {
            "id": None,
            "title": "Network Infrastructure Knowledge Graph",
            "tags": ["infrastructure", "network", "kubernetes"],
            "timezone": "browser",
            "panels": [
                {
                    "id": 1,
                    "title": "Entity Count by Type",
                    "type": "piechart",
                    "targets": [
                        {
                            "expr": """
                            MATCH (n)
                            RETURN labels(n)[1] as entity_type, count(n) as count
                            ORDER BY count DESC
                            """,
                            "format": "table"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
                },
                {
                    "id": 2,
                    "title": "Relationship Distribution",
                    "type": "barchart",
                    "targets": [
                        {
                            "expr": """
                            MATCH ()-[r]->()
                            RETURN type(r) as relationship_type, count(r) as count
                            ORDER BY count DESC
                            """,
                            "format": "table"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
                },
                {
                    "id": 3,
                    "title": "Infrastructure Topology Metrics",
                    "type": "stat",
                    "targets": [
                        {
                            "expr": """
                            MATCH (n)
                            RETURN 
                                count(n) as total_entities,
                                count(DISTINCT labels(n)[1]) as entity_types
                            """,
                            "format": "table"
                        }
                    ],
                    "gridPos": {"h": 4, "w": 24, "x": 0, "y": 8}
                },
                {
                    "id": 4,
                    "title": "Resource Utilization",
                    "type": "gauge",
                    "targets": [
                        {
                            "expr": """
                            MATCH (s:Server)
                            RETURN 
                                sum(s.cpu_cores) as total_cpu_cores,
                                sum(s.memory_gb) as total_memory_gb,
                                count(s) as server_count
                            """,
                            "format": "table"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 12}
                },
                {
                    "id": 5,
                    "title": "Container Distribution by Namespace",
                    "type": "table",
                    "targets": [
                        {
                            "expr": """
                            MATCH (p:KubernetesPod)
                            RETURN p.namespace as namespace, count(p) as pod_count
                            ORDER BY pod_count DESC
                            """,
                            "format": "table"
                        }
                    ],
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 12}
                }
            ],
            "time": {"from": "now-1h", "to": "now"},
            "refresh": "30s"
        }
    }
    
    grafana_file = os.path.join(output_dir, "grafana_dashboard.json")
    
    import json
    with open(grafana_file, 'w') as f:
        json.dump(grafana_config, f, indent=2)
    
    print(f"✅ Grafana dashboard config saved to: {grafana_file}")


if __name__ == "__main__":
    main() 