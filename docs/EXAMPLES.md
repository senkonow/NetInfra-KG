# 📋 Examples and Use Cases

## Overview

This document provides practical examples and real-world use cases for the Network Infrastructure Knowledge Graph system. Each example includes complete code and explanations.

---

## 🏗️ Basic Usage Examples

### Example 1: Setting Up Your First Knowledge Graph

```python
from kg.database import Neo4jKnowledgeGraph
from kg.data_generator import InfrastructureDataGenerator
from kg.models import EntityType

# Initialize the knowledge graph
kg = Neo4jKnowledgeGraph()

# Set up the database schema
kg.setup_constraints_and_indexes()

# Generate sample infrastructure data
generator = InfrastructureDataGenerator(kg)
counts = generator.populate_database()

print(f"Created infrastructure with {sum(counts.values())} total entities:")
for entity_type, count in counts.items():
    print(f"  {entity_type}: {count}")

# Get some basic statistics
stats = kg.get_statistics()
print(f"\nDatabase Statistics:")
print(f"  Total entities: {stats['total_entities']}")
print(f"  Total relationships: {stats['total_relationships']}")
```

### Example 2: Querying Infrastructure Data

```python
from kg.database import Neo4jKnowledgeGraph
from kg.models import EntityType

kg = Neo4jKnowledgeGraph()

# Find all servers
servers = kg.query_entities_by_type(EntityType.SERVER)
print(f"Found {len(servers)} servers:")
for server in servers[:3]:  # Show first 3
    print(f"  {server['name']} - {server['hostname']} ({server['cpu_cores']} cores)")

# Find containers with high memory usage
high_memory_containers = kg.execute_query("""
    MATCH (c:Container) 
    WHERE c.memory_mb > 512 
    RETURN c.name as name, c.memory_mb as memory, c.image as image
    ORDER BY c.memory_mb DESC
    LIMIT 10
""")

print(f"\nHigh memory containers:")
for container in high_memory_containers:
    print(f"  {container['name']}: {container['memory']}MB ({container['image']})")
```

### Example 3: Path Analysis

```python
from kg.database import Neo4jKnowledgeGraph
from kg.models import EntityType

kg = Neo4jKnowledgeGraph()

# Get some entities for path analysis
containers = kg.query_entities_by_type(EntityType.CONTAINER)
servers = kg.query_entities_by_type(EntityType.SERVER)

if containers and servers:
    container_id = containers[0]['id']
    server_id = servers[0]['id']
    
    # Find the path from container to server
    path = kg.get_topology_path(container_id, server_id)
    
    if path:
        print(f"Path from {containers[0]['name']} to {servers[0]['name']}:")
        for i, step in enumerate(path):
            print(f"  {i+1}. {step['entity_type']}: {step['name']}")
            if i < len(path) - 1:
                print(f"     ↓ ({step['relationship_type']})")
    else:
        print("No path found between container and server")
```

---

## 🎨 Visualization Examples

### Example 4: Creating Multiple Visualizations

```python
from kg.database import Neo4jKnowledgeGraph
from kg.visualization import GraphVisualizer
import os

kg = Neo4jKnowledgeGraph()
visualizer = GraphVisualizer(kg)

# Create output directory
os.makedirs("my_visualizations", exist_ok=True)

# 1. Full network interactive visualization
print("Creating full network visualization...")
visualizer.create_pyvis_network(
    output_file="my_visualizations/full_network.html"
)

# 2. Server-focused visualization
print("Creating server-focused visualization...")
visualizer.create_pyvis_network(
    filter_entities=["Server", "VirtualMachine"],
    output_file="my_visualizations/servers_only.html"
)

# 3. Container ecosystem visualization
print("Creating container ecosystem visualization...")
visualizer.create_pyvis_network(
    filter_entities=["KubernetesPod", "Container"],
    output_file="my_visualizations/containers_only.html"
)

# 4. Static network image
print("Creating static network image...")
visualizer.create_matplotlib_static(
    output_file="my_visualizations/network_topology.png"
)

# 5. Interactive Plotly visualization
print("Creating Plotly visualization...")
fig = visualizer.create_plotly_network(layout_algorithm="circular")
fig.write_html("my_visualizations/plotly_network.html")

# 6. Hierarchy chart
print("Creating hierarchy chart...")
visualizer.create_hierarchy_chart(
    output_file="my_visualizations/entity_hierarchy.html"
)

print("All visualizations created in 'my_visualizations/' directory!")
```

### Example 5: Custom Visualization with Filters

```python
from kg.database import Neo4jKnowledgeGraph
from kg.visualization import GraphVisualizer

kg = Neo4jKnowledgeGraph()
viz = GraphVisualizer(kg)

# Create a production-focused visualization
production_servers = kg.execute_query("""
    MATCH (s:Server) 
    WHERE s.hostname CONTAINS 'prod'
    RETURN s.id as id
""")

if production_servers:
    print("Creating production infrastructure visualization...")
    # Note: This would require extending the visualizer to support entity ID filtering
    # For now, we'll create a filtered view by entity type
    viz.create_pyvis_network(
        filter_entities=["Server", "VirtualMachine", "Container"],
        output_file="production_infrastructure.html"
    )
else:
    print("No production servers found")
```

---

## 🤖 LLM Integration Examples

### Example 6: Natural Language Queries

```python
from kg.database import Neo4jKnowledgeGraph
from kg.llm_interface import KnowledgeGraphLLMInterface

kg = Neo4jKnowledgeGraph()
llm = KnowledgeGraphLLMInterface(kg)

# Ask various questions in natural language
questions = [
    "What is the topology overview?",
    "Show me server resources",
    "What are the container details?",
    "Show me the network overview",
    "What are the security contexts?"
]

for question in questions:
    print(f"\nQ: {question}")
    print("A:", llm.query_natural_language(question))
    print("-" * 50)
```

### Example 7: Data Export for AI Training

```python
from kg.database import Neo4jKnowledgeGraph
from kg.llm_interface import KnowledgeGraphLLMInterface
import json
from datetime import datetime

kg = Neo4jKnowledgeGraph()
llm = KnowledgeGraphLLMInterface(kg)

# Export data in different formats
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# 1. JSON export for structured AI consumption
print("Exporting JSON data for AI training...")
json_data = llm.export_for_llm_training("json")
with open(f"ai_training_data_{timestamp}.json", "w") as f:
    f.write(json_data)

# 2. Text export for human-readable format
print("Exporting text data for documentation...")
text_data = llm.export_for_llm_training("text")
with open(f"infrastructure_report_{timestamp}.txt", "w") as f:
    f.write(text_data)

# 3. Custom export with specific focus
print("Creating custom export with server focus...")
custom_data = {
    "export_timestamp": timestamp,
    "topology_summary": llm.get_topology_summary(),
    "server_resources": llm.query_natural_language("Show me server resources"),
    "container_overview": llm.query_natural_language("What are the container details?")
}

with open(f"custom_export_{timestamp}.json", "w") as f:
    json.dump(custom_data, f, indent=2)

print(f"Exported data with timestamp: {timestamp}")
```

---

## 🔍 Advanced Query Examples

### Example 8: Resource Utilization Analysis

```python
from kg.database import Neo4jKnowledgeGraph

kg = Neo4jKnowledgeGraph()

# Analyze server resource utilization
resource_analysis = kg.execute_query("""
    MATCH (s:Server)
    OPTIONAL MATCH (s)-[:HOSTS]->(vm:VirtualMachine)
    OPTIONAL MATCH (vm)-[:RUNS_ON]->(pod:KubernetesPod)
    OPTIONAL MATCH (pod)-[:CONTAINS]->(c:Container)
    
    RETURN 
        s.name as server_name,
        s.cpu_cores as server_cpu,
        s.memory_gb as server_memory,
        count(DISTINCT vm) as vm_count,
        count(DISTINCT pod) as pod_count,
        count(DISTINCT c) as container_count,
        sum(vm.cpu_cores) as allocated_cpu,
        sum(vm.memory_gb) as allocated_memory
    ORDER BY server_cpu DESC
""")

print("Server Resource Utilization Analysis:")
print("-" * 80)
for server in resource_analysis:
    cpu_utilization = (server['allocated_cpu'] / server['server_cpu']) * 100 if server['allocated_cpu'] else 0
    memory_utilization = (server['allocated_memory'] / server['server_memory']) * 100 if server['allocated_memory'] else 0
    
    print(f"Server: {server['server_name']}")
    print(f"  Hardware: {server['server_cpu']} cores, {server['server_memory']}GB RAM")
    print(f"  Workload: {server['vm_count']} VMs, {server['pod_count']} pods, {server['container_count']} containers")
    print(f"  CPU Utilization: {cpu_utilization:.1f}%")
    print(f"  Memory Utilization: {memory_utilization:.1f}%")
    print()
```

### Example 9: Network Topology Analysis

```python
from kg.database import Neo4jKnowledgeGraph

kg = Neo4jKnowledgeGraph()

# Analyze network topology and connectivity
network_analysis = kg.execute_query("""
    MATCH (sw:NetworkSwitch)
    OPTIONAL MATCH (sw)-[:CONTAINS]->(p:NetworkPort)
    OPTIONAL MATCH (p)-[:BELONGS_TO]->(v:VLAN)
    
    RETURN 
        sw.name as switch_name,
        sw.hostname as switch_hostname,
        count(DISTINCT p) as port_count,
        count(DISTINCT v) as vlan_count,
        collect(DISTINCT v.name) as vlan_names
    ORDER BY port_count DESC
""")

print("Network Topology Analysis:")
print("-" * 60)
for switch in network_analysis:
    print(f"Switch: {switch['switch_name']} ({switch['switch_hostname']})")
    print(f"  Ports: {switch['port_count']}")
    print(f"  VLANs: {switch['vlan_count']}")
    if switch['vlan_names']:
        print(f"  VLAN Names: {', '.join(switch['vlan_names'][:5])}")
    print()
```

### Example 10: Security Context Analysis

```python
from kg.database import Neo4jKnowledgeGraph

kg = Neo4jKnowledgeGraph()

# Analyze security contexts and network segments
security_analysis = kg.execute_query("""
    MATCH (v:VLAN)
    OPTIONAL MATCH (v)<-[:BELONGS_TO]-(entity)
    
    RETURN 
        v.name as vlan_name,
        v.vlan_id as vlan_id,
        count(entity) as connected_entities,
        collect(DISTINCT labels(entity)[0]) as entity_types
    ORDER BY connected_entities DESC
""")

print("Security Context Analysis (VLAN Segmentation):")
print("-" * 70)
for vlan in security_analysis:
    print(f"VLAN: {vlan['vlan_name']} (ID: {vlan['vlan_id']})")
    print(f"  Connected Entities: {vlan['connected_entities']}")
    print(f"  Entity Types: {', '.join(vlan['entity_types'])}")
    print()
```

---

## 🔧 Custom Entity Examples

### Example 11: Adding Custom Entity Types

```python
from kg.models import BaseEntity, EntityType
from kg.database import Neo4jKnowledgeGraph
from pydantic import Field
from typing import Optional, List
from enum import Enum

# Extend EntityType enum
class CustomEntityType(str, Enum):
    LOAD_BALANCER = "LoadBalancer"
    DATABASE = "Database"
    MONITORING_AGENT = "MonitoringAgent"

# Define custom entity models
class LoadBalancer(BaseEntity):
    type: CustomEntityType = Field(default=CustomEntityType.LOAD_BALANCER, const=True)
    algorithm: str = Field(description="Load balancing algorithm")
    backend_servers: List[str] = Field(description="Backend server IDs")
    health_check_url: Optional[str] = Field(None, description="Health check endpoint")
    ssl_enabled: bool = Field(default=True, description="SSL/TLS enabled")

class Database(BaseEntity):
    type: CustomEntityType = Field(default=CustomEntityType.DATABASE, const=True)
    engine: str = Field(description="Database engine (MySQL, PostgreSQL, etc.)")
    version: str = Field(description="Database version")
    port: int = Field(description="Database port")
    storage_size_gb: int = Field(description="Storage size in GB")
    backup_enabled: bool = Field(default=True, description="Backup enabled")

# Create and store custom entities
kg = Neo4jKnowledgeGraph()

# Create a load balancer
lb = LoadBalancer(
    name="Main-LoadBalancer",
    algorithm="round_robin",
    backend_servers=["server-01", "server-02", "server-03"],
    health_check_url="/health",
    ssl_enabled=True
)

# Create a database
db = Database(
    name="Primary-Database",
    engine="PostgreSQL",
    version="13.7",
    port=5432,
    storage_size_gb=500,
    backup_enabled=True
)

# Store in knowledge graph
kg.create_entity(lb)
kg.create_entity(db)

print(f"Created custom entities:")
print(f"  Load Balancer: {lb.name}")
print(f"  Database: {db.name}")
```

### Example 12: Custom Relationships

```python
from kg.models import RelationshipType, BaseRelationship
from kg.database import Neo4jKnowledgeGraph
from pydantic import Field

# Extend relationship types
class CustomRelationshipType(str, Enum):
    LOAD_BALANCES = "LOAD_BALANCES"
    MONITORS = "MONITORS"
    BACKS_UP = "BACKS_UP"

# Create custom relationships
kg = Neo4jKnowledgeGraph()

# Get entities for relationship creation
servers = kg.query_entities_by_type(EntityType.SERVER)
if len(servers) >= 2:
    # Create load balancing relationship
    kg.create_relationship(
        source_id="main-loadbalancer",  # Load balancer ID
        target_id=servers[0]['id'],
        relationship_type=CustomRelationshipType.LOAD_BALANCES,
        properties={
            "weight": 100,
            "active": True,
            "health_status": "healthy"
        }
    )
    
    print("Created custom load balancing relationship")
```

---

## 🚀 Production Use Cases

### Example 13: Infrastructure Monitoring Dashboard

```python
from kg.database import Neo4jKnowledgeGraph
from kg.llm_interface import KnowledgeGraphLLMInterface
import json
from datetime import datetime

class InfrastructureMonitor:
    def __init__(self):
        self.kg = Neo4jKnowledgeGraph()
        self.llm = KnowledgeGraphLLMInterface(self.kg)
    
    def generate_health_report(self):
        """Generate a comprehensive infrastructure health report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.llm.get_topology_summary(),
            "alerts": self.check_resource_alerts(),
            "recommendations": self.generate_recommendations()
        }
        return report
    
    def check_resource_alerts(self):
        """Check for resource utilization alerts"""
        alerts = []
        
        # Check for high CPU usage
        high_cpu_containers = self.kg.execute_query("""
            MATCH (c:Container) 
            WHERE c.cpu_cores > 2 
            RETURN c.name as name, c.cpu_cores as cpu
        """)
        
        if high_cpu_containers:
            alerts.append({
                "type": "high_cpu",
                "message": f"Found {len(high_cpu_containers)} containers with high CPU usage",
                "details": high_cpu_containers
            })
        
        # Check for high memory usage
        high_memory_containers = self.kg.execute_query("""
            MATCH (c:Container) 
            WHERE c.memory_mb > 1024 
            RETURN c.name as name, c.memory_mb as memory
        """)
        
        if high_memory_containers:
            alerts.append({
                "type": "high_memory",
                "message": f"Found {len(high_memory_containers)} containers with high memory usage",
                "details": high_memory_containers
            })
        
        return alerts
    
    def generate_recommendations(self):
        """Generate optimization recommendations"""
        recommendations = []
        
        # Check for underutilized servers
        server_stats = self.kg.execute_query("""
            MATCH (s:Server)
            OPTIONAL MATCH (s)-[:HOSTS]->(vm:VirtualMachine)
            RETURN s.name as server, count(vm) as vm_count, s.cpu_cores as cpu
            ORDER BY vm_count ASC
        """)
        
        for server in server_stats:
            if server['vm_count'] < 2 and server['cpu'] > 8:
                recommendations.append({
                    "type": "underutilized_server",
                    "message": f"Server {server['server']} may be underutilized",
                    "details": f"Only {server['vm_count']} VMs on {server['cpu']}-core server"
                })
        
        return recommendations

# Usage
monitor = InfrastructureMonitor()
report = monitor.generate_health_report()

print("Infrastructure Health Report")
print("=" * 50)
print(f"Generated at: {report['timestamp']}")
print(f"Total entities: {report['summary']['infrastructure_overview']['total_entities']}")

print("\nAlerts:")
for alert in report['alerts']:
    print(f"  - {alert['message']}")

print("\nRecommendations:")
for rec in report['recommendations']:
    print(f"  - {rec['message']}")
```

### Example 14: Capacity Planning Tool

```python
from kg.database import Neo4jKnowledgeGraph
import json

class CapacityPlanner:
    def __init__(self):
        self.kg = Neo4jKnowledgeGraph()
    
    def analyze_capacity(self):
        """Analyze current capacity and predict growth"""
        # Get current resource usage
        resource_usage = self.kg.execute_query("""
            MATCH (s:Server)
            OPTIONAL MATCH (s)-[:HOSTS]->(vm:VirtualMachine)
            OPTIONAL MATCH (vm)-[:RUNS_ON]->(pod:KubernetesPod)
            OPTIONAL MATCH (pod)-[:CONTAINS]->(c:Container)
            
            RETURN 
                s.name as server,
                s.cpu_cores as total_cpu,
                s.memory_gb as total_memory,
                count(DISTINCT vm) as vms,
                count(DISTINCT c) as containers,
                sum(vm.cpu_cores) as allocated_cpu,
                sum(vm.memory_gb) as allocated_memory
        """)
        
        capacity_report = {
            "servers": [],
            "cluster_totals": {
                "total_cpu": 0,
                "total_memory": 0,
                "allocated_cpu": 0,
                "allocated_memory": 0
            }
        }
        
        for server in resource_usage:
            server_data = {
                "name": server['server'],
                "cpu_utilization": (server['allocated_cpu'] / server['total_cpu']) * 100 if server['allocated_cpu'] else 0,
                "memory_utilization": (server['allocated_memory'] / server['total_memory']) * 100 if server['allocated_memory'] else 0,
                "workload": {
                    "vms": server['vms'],
                    "containers": server['containers']
                }
            }
            capacity_report['servers'].append(server_data)
            
            # Update cluster totals
            capacity_report['cluster_totals']['total_cpu'] += server['total_cpu']
            capacity_report['cluster_totals']['total_memory'] += server['total_memory']
            capacity_report['cluster_totals']['allocated_cpu'] += server['allocated_cpu'] or 0
            capacity_report['cluster_totals']['allocated_memory'] += server['allocated_memory'] or 0
        
        return capacity_report
    
    def predict_growth(self, growth_rate=0.1):
        """Predict capacity needs based on growth rate"""
        current_capacity = self.analyze_capacity()
        
        predictions = {
            "current": current_capacity,
            "predicted_6_months": self.calculate_future_needs(current_capacity, 6, growth_rate),
            "predicted_12_months": self.calculate_future_needs(current_capacity, 12, growth_rate)
        }
        
        return predictions
    
    def calculate_future_needs(self, current, months, growth_rate):
        """Calculate future resource needs"""
        multiplier = (1 + growth_rate) ** (months / 12)
        
        return {
            "cpu_needed": current['cluster_totals']['allocated_cpu'] * multiplier,
            "memory_needed": current['cluster_totals']['allocated_memory'] * multiplier,
            "additional_servers_needed": max(0, int((current['cluster_totals']['allocated_cpu'] * multiplier) / 16) - len(current['servers']))
        }

# Usage
planner = CapacityPlanner()
predictions = planner.predict_growth(growth_rate=0.15)  # 15% annual growth

print("Capacity Planning Report")
print("=" * 40)
print(f"Current cluster CPU utilization: {predictions['current']['cluster_totals']['allocated_cpu']}/{predictions['current']['cluster_totals']['total_cpu']}")
print(f"Current cluster memory utilization: {predictions['current']['cluster_totals']['allocated_memory']}/{predictions['current']['cluster_totals']['total_memory']}")

print("\n6-month predictions:")
print(f"  CPU needed: {predictions['predicted_6_months']['cpu_needed']:.1f} cores")
print(f"  Memory needed: {predictions['predicted_6_months']['memory_needed']:.1f} GB")
print(f"  Additional servers needed: {predictions['predicted_6_months']['additional_servers_needed']}")

print("\n12-month predictions:")
print(f"  CPU needed: {predictions['predicted_12_months']['cpu_needed']:.1f} cores")
print(f"  Memory needed: {predictions['predicted_12_months']['memory_needed']:.1f} GB")
print(f"  Additional servers needed: {predictions['predicted_12_months']['additional_servers_needed']}")
```

### Example 15: Compliance and Audit Tool

```python
from kg.database import Neo4jKnowledgeGraph
from datetime import datetime

class ComplianceAuditor:
    def __init__(self):
        self.kg = Neo4jKnowledgeGraph()
    
    def run_compliance_audit(self):
        """Run comprehensive compliance audit"""
        audit_report = {
            "timestamp": datetime.now().isoformat(),
            "checks": [],
            "summary": {"passed": 0, "failed": 0, "warnings": 0}
        }
        
        # Check 1: All servers should have monitoring
        audit_report["checks"].append(self.check_server_monitoring())
        
        # Check 2: Network segmentation
        audit_report["checks"].append(self.check_network_segmentation())
        
        # Check 3: Resource limits
        audit_report["checks"].append(self.check_resource_limits())
        
        # Calculate summary
        for check in audit_report["checks"]:
            audit_report["summary"][check["status"]] += 1
        
        return audit_report
    
    def check_server_monitoring(self):
        """Check if all servers have proper monitoring"""
        servers_without_monitoring = self.kg.execute_query("""
            MATCH (s:Server)
            WHERE NOT EXISTS {
                MATCH (s)-[:MONITORS]-(m:MonitoringAgent)
            }
            RETURN s.name as server
        """)
        
        return {
            "name": "Server Monitoring",
            "status": "failed" if servers_without_monitoring else "passed",
            "details": f"Found {len(servers_without_monitoring)} servers without monitoring",
            "affected_entities": [s['server'] for s in servers_without_monitoring]
        }
    
    def check_network_segmentation(self):
        """Check network segmentation compliance"""
        vlan_distribution = self.kg.execute_query("""
            MATCH (v:VLAN)
            OPTIONAL MATCH (v)<-[:BELONGS_TO]-(entity)
            RETURN v.name as vlan, count(entity) as entity_count
            ORDER BY entity_count DESC
        """)
        
        # Check if any VLAN has too many entities (potential security risk)
        oversized_vlans = [v for v in vlan_distribution if v['entity_count'] > 20]
        
        return {
            "name": "Network Segmentation",
            "status": "warning" if oversized_vlans else "passed",
            "details": f"Found {len(oversized_vlans)} VLANs with excessive entities",
            "affected_entities": [v['vlan'] for v in oversized_vlans]
        }
    
    def check_resource_limits(self):
        """Check if containers have proper resource limits"""
        unlimited_containers = self.kg.execute_query("""
            MATCH (c:Container)
            WHERE c.cpu_cores > 4 OR c.memory_mb > 2048
            RETURN c.name as container, c.cpu_cores as cpu, c.memory_mb as memory
        """)
        
        return {
            "name": "Resource Limits",
            "status": "warning" if unlimited_containers else "passed",
            "details": f"Found {len(unlimited_containers)} containers with high resource allocation",
            "affected_entities": [c['container'] for c in unlimited_containers]
        }

# Usage
auditor = ComplianceAuditor()
audit_report = auditor.run_compliance_audit()

print("Compliance Audit Report")
print("=" * 50)
print(f"Generated at: {audit_report['timestamp']}")
print(f"Summary: {audit_report['summary']['passed']} passed, {audit_report['summary']['failed']} failed, {audit_report['summary']['warnings']} warnings")

print("\nDetailed Results:")
for check in audit_report['checks']:
    status_emoji = {"passed": "✅", "failed": "❌", "warning": "⚠️"}
    print(f"{status_emoji[check['status']]} {check['name']}: {check['details']}")
    if check['affected_entities']:
        print(f"   Affected: {', '.join(check['affected_entities'][:5])}")
```

---

## 📊 Integration Examples

### Example 16: Integration with External APIs

```python
import requests
from kg.database import Neo4jKnowledgeGraph
from kg.models import Server, Container
import json

class ExternalDataIntegrator:
    def __init__(self):
        self.kg = Neo4jKnowledgeGraph()
    
    def sync_with_kubernetes_api(self, k8s_api_url, auth_token):
        """Sync with Kubernetes API to get real container data"""
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        try:
            # Get pods from Kubernetes API
            response = requests.get(f"{k8s_api_url}/api/v1/pods", headers=headers)
            pods_data = response.json()
            
            # Update knowledge graph with real data
            for pod in pods_data.get('items', []):
                self.update_pod_data(pod)
                
        except Exception as e:
            print(f"Error syncing with Kubernetes: {e}")
    
    def update_pod_data(self, pod_data):
        """Update pod data in knowledge graph"""
        pod_name = pod_data['metadata']['name']
        
        # Find existing pod in knowledge graph
        existing_pod = self.kg.execute_query("""
            MATCH (p:KubernetesPod {name: $name})
            RETURN p.id as id
        """, {"name": pod_name})
        
        if existing_pod:
            pod_id = existing_pod[0]['id']
            
            # Update with real status
            self.kg.execute_query("""
                MATCH (p:KubernetesPod {id: $id})
                SET p.status = $status,
                    p.last_updated = datetime()
            """, {
                "id": pod_id,
                "status": pod_data['status']['phase']
            })
    
    def integrate_monitoring_data(self, monitoring_endpoint):
        """Integrate with monitoring system (e.g., Prometheus)"""
        try:
            # Example: Get CPU usage metrics
            cpu_query = "avg(cpu_usage_rate) by (container_name)"
            response = requests.get(f"{monitoring_endpoint}/api/v1/query", {
                'query': cpu_query
            })
            
            metrics_data = response.json()
            
            # Update containers with real metrics
            for result in metrics_data.get('data', {}).get('result', []):
                container_name = result['metric']['container_name']
                cpu_usage = float(result['value'][1])
                
                self.kg.execute_query("""
                    MATCH (c:Container {name: $name})
                    SET c.current_cpu_usage = $usage,
                        c.last_metric_update = datetime()
                """, {
                    "name": container_name,
                    "usage": cpu_usage
                })
                
        except Exception as e:
            print(f"Error integrating monitoring data: {e}")

# Usage example (with mock data)
integrator = ExternalDataIntegrator()
print("External data integration example setup complete")
```

---

## 🧪 Testing Examples

### Example 17: Unit Testing Your Knowledge Graph

```python
import unittest
from kg.database import Neo4jKnowledgeGraph
from kg.models import Server, Container, EntityType
from kg.data_generator import InfrastructureDataGenerator

class TestKnowledgeGraph(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.kg = Neo4jKnowledgeGraph()
        # Clear database for testing
        self.kg.execute_query("MATCH (n) DETACH DELETE n")
        self.kg.setup_constraints_and_indexes()
    
    def test_entity_creation(self):
        """Test creating entities"""
        server = Server(
            name="test-server",
            hostname="test.example.com",
            cpu_cores=8,
            memory_gb=16,
            storage_gb=500,
            operating_system="Ubuntu 20.04"
        )
        
        result = self.kg.create_entity(server)
        
        # Verify entity was created
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], "test-server")
        self.assertEqual(result['cpu_cores'], 8)
    
    def test_entity_queries(self):
        """Test querying entities"""
        # Create test data
        generator = InfrastructureDataGenerator(self.kg)
        counts = generator.populate_database()
        
        # Test query by type
        servers = self.kg.query_entities_by_type(EntityType.SERVER)
        self.assertEqual(len(servers), counts['servers'])
        
        containers = self.kg.query_entities_by_type(EntityType.CONTAINER)
        self.assertEqual(len(containers), counts['containers'])
    
    def test_relationship_creation(self):
        """Test creating relationships"""
        # Create two entities
        server = Server(name="server1", hostname="server1.com", cpu_cores=4)
        container = Container(name="container1", image="nginx:latest", cpu_cores=1)
        
        server_result = self.kg.create_entity(server)
        container_result = self.kg.create_entity(container)
        
        # Create relationship
        rel = self.kg.create_relationship(
            source_id=server_result['id'],
            target_id=container_result['id'],
            relationship_type=RelationshipType.HOSTS
        )
        
        self.assertIsNotNone(rel)
    
    def test_path_finding(self):
        """Test topology path finding"""
        # Create test topology
        generator = InfrastructureDataGenerator(self.kg)
        generator.populate_database()
        
        # Get entities for path testing
        containers = self.kg.query_entities_by_type(EntityType.CONTAINER)
        servers = self.kg.query_entities_by_type(EntityType.SERVER)
        
        if containers and servers:
            path = self.kg.get_topology_path(containers[0]['id'], servers[0]['id'])
            self.assertIsNotNone(path)
            self.assertGreater(len(path), 0)
    
    def tearDown(self):
        """Clean up after tests"""
        self.kg.execute_query("MATCH (n) DETACH DELETE n")

# Run tests
if __name__ == '__main__':
    unittest.main()
```

---

This examples document provides comprehensive code samples for various use cases of the Knowledge Graph system. Each example is designed to be practical and immediately usable, demonstrating both basic functionality and advanced integration patterns. 