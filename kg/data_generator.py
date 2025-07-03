"""
Sample data generator for network infrastructure topology
"""
import random
import string
from typing import List, Tuple
from datetime import datetime

from .models import (
    NetworkSwitch, NetworkPort, VLAN, Server, VirtualMachine,
    KubernetesPod, Container, Relationship, RelationshipType
)
from .database import Neo4jKnowledgeGraph


class InfrastructureDataGenerator:
    """Generate sample network infrastructure data"""
    
    def __init__(self, kg: Neo4jKnowledgeGraph):
        self.kg = kg
        self.entities = []
        self.relationships = []
    
    def generate_id(self, prefix: str) -> str:
        """Generate a unique ID with prefix"""
        return f"{prefix}-{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}"
    
    def generate_ip_address(self, subnet: str = "10.0") -> str:
        """Generate a random IP address"""
        return f"{subnet}.{random.randint(1, 254)}.{random.randint(1, 254)}"
    
    def generate_mac_address(self) -> str:
        """Generate a random MAC address"""
        return ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])
    
    def create_network_switches(self, count: int = 3) -> List[NetworkSwitch]:
        """Create network switches"""
        switches = []
        vendors = ["Cisco", "Juniper", "Arista", "HP", "Dell"]
        models = ["Catalyst 9300", "EX4300", "7050X", "ProCurve 2920", "PowerSwitch S3048"]
        locations = ["DataCenter-A", "DataCenter-B", "Edge-01", "Core-01", "Dist-01"]
        
        for i in range(count):
            switch = NetworkSwitch(
                id=self.generate_id("sw"),
                name=f"Switch-{i+1:02d}",
                vendor=random.choice(vendors),
                model=random.choice(models),
                ip_address=self.generate_ip_address("192.168.1"),
                mac_address=self.generate_mac_address(),
                port_count=random.choice([24, 48, 72]),
                location=random.choice(locations)
            )
            switches.append(switch)
            self.entities.append(switch)
        
        return switches
    
    def create_network_ports(self, switches: List[NetworkSwitch], ports_per_switch: int = 24) -> List[NetworkPort]:
        """Create network ports for switches"""
        ports = []
        port_types = ["GigabitEthernet", "TenGigabitEthernet", "FastEthernet"]
        
        for switch in switches:
            for port_num in range(1, ports_per_switch + 1):
                port = NetworkPort(
                    id=self.generate_id("port"),
                    name=f"{switch.name}-Port-{port_num:02d}",
                    port_number=port_num,
                    port_type=random.choice(port_types),
                    status=random.choice(["up", "down"]),
                    speed=random.choice(["1000Mbps", "100Mbps", "10Gbps"]),
                    duplex=random.choice(["full", "half"])
                )
                ports.append(port)
                self.entities.append(port)
                
                # Create relationship: Switch -> Port
                rel = Relationship(
                    source_id=switch.id,
                    target_id=port.id,
                    relationship_type=RelationshipType.CONTAINS
                )
                rel.set_properties({"port_number": port_num})
                self.relationships.append(rel)
        
        return ports
    
    def create_vlans(self, count: int = 10) -> List[VLAN]:
        """Create VLANs"""
        vlans = []
        vlan_names = ["Management", "Production", "Development", "DMZ", "Guest", "Storage", "Backup", "Security", "IoT", "Voice"]
        
        for i, name in enumerate(vlan_names[:count]):
            vlan_id = random.randint(10, 4094)
            vlan = VLAN(
                id=self.generate_id("vlan"),
                name=f"VLAN-{name}",
                vlan_id=vlan_id,
                subnet=f"10.{vlan_id//100}.{vlan_id%100}.0/24",
                gateway=f"10.{vlan_id//100}.{vlan_id%100}.1",
                description=f"{name} VLAN"
            )
            vlans.append(vlan)
            self.entities.append(vlan)
        
        return vlans
    
    def create_servers(self, count: int = 5) -> List[Server]:
        """Create physical servers"""
        servers = []
        os_types = ["Ubuntu 20.04", "RHEL 8", "CentOS 7", "Windows Server 2019", "VMware ESXi 7.0"]
        
        for i in range(count):
            server = Server(
                id=self.generate_id("srv"),
                name=f"Server-{i+1:02d}",
                hostname=f"srv-{i+1:02d}.example.com",
                ip_address=self.generate_ip_address("10.1"),
                mac_address=self.generate_mac_address(),
                cpu_cores=random.choice([16, 32, 64, 128]),
                memory_gb=random.choice([64, 128, 256, 512]),
                storage_gb=random.choice([1000, 2000, 4000, 8000]),
                os=random.choice(os_types),
                rack_location=f"Rack-{random.randint(1, 20)}-U{random.randint(1, 42)}"
            )
            servers.append(server)
            self.entities.append(server)
        
        return servers
    
    def create_virtual_machines(self, servers: List[Server], vms_per_server: int = 10) -> List[VirtualMachine]:
        """Create virtual machines on servers"""
        vms = []
        vm_os_types = ["Ubuntu 20.04", "Ubuntu 22.04", "CentOS 8", "Windows 10", "Windows Server 2019"]
        hypervisors = ["VMware vSphere", "KVM", "Hyper-V", "Xen"]
        
        for server in servers:
            for vm_num in range(1, vms_per_server + 1):
                vm = VirtualMachine(
                    id=self.generate_id("vm"),
                    name=f"{server.name}-VM-{vm_num:02d}",
                    hostname=f"vm-{server.name.lower()}-{vm_num:02d}.example.com",
                    ip_address=self.generate_ip_address("10.2"),
                    cpu_cores=random.choice([2, 4, 8, 16]),
                    memory_gb=random.choice([4, 8, 16, 32]),
                    storage_gb=random.choice([50, 100, 200, 500]),
                    os=random.choice(vm_os_types),
                    hypervisor=random.choice(hypervisors),
                    vm_id=self.generate_id("vmid")
                )
                vms.append(vm)
                self.entities.append(vm)
                
                # Create relationship: Server -> VM
                rel = Relationship(
                    source_id=server.id,
                    target_id=vm.id,
                    relationship_type=RelationshipType.HOSTS
                )
                rel.set_properties({"hypervisor": vm.hypervisor})
                self.relationships.append(rel)
        
        return vms
    
    def create_kubernetes_pods(self, vms: List[VirtualMachine], pods_per_vm: int = 100) -> List[KubernetesPod]:
        """Create Kubernetes pods on VMs"""
        pods = []
        namespaces = ["default", "kube-system", "production", "staging", "development", "monitoring", "logging"]
        phases = ["Running", "Pending", "Succeeded", "Failed", "Unknown"]
        
        # Only create pods on some VMs (those that would be k8s nodes)
        k8s_vms = random.sample(vms, min(len(vms), 3))
        
        for vm in k8s_vms:
            for pod_num in range(1, pods_per_vm + 1):
                namespace = random.choice(namespaces)
                pod = KubernetesPod(
                    id=self.generate_id("pod"),
                    name=f"pod-{namespace}-{pod_num:03d}",
                    namespace=namespace,
                    pod_ip=self.generate_ip_address("10.244"),
                    node_name=vm.hostname,
                    phase=random.choice(phases),
                    restart_count=random.randint(0, 10)
                )
                
                # Set k8s labels and annotations using the new methods
                pod.set_k8s_labels({
                    "app": f"app-{random.randint(1, 10)}",
                    "version": f"v{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
                    "environment": random.choice(["prod", "staging", "dev"])
                })
                
                pod.set_annotations({
                    "created-by": "deployment-controller",
                    "last-restart": datetime.now().isoformat()
                })
                pods.append(pod)
                self.entities.append(pod)
                
                # Create relationship: VM -> Pod
                rel = Relationship(
                    source_id=vm.id,
                    target_id=pod.id,
                    relationship_type=RelationshipType.RUNS_ON
                )
                rel.set_properties({"namespace": namespace, "node": vm.hostname})
                self.relationships.append(rel)
        
        return pods
    
    def create_containers(self, pods: List[KubernetesPod], containers_per_pod: int = 1000) -> List[Container]:
        """Create containers in pods"""
        containers = []
        images = [
            "nginx:latest", "redis:6.2", "postgres:13", "mysql:8.0", "mongodb:4.4",
            "elasticsearch:7.15", "kibana:7.15", "prometheus:latest", "grafana:latest",
            "jenkins:latest", "node:16-alpine", "python:3.9-slim", "openjdk:11-jre"
        ]
        statuses = ["running", "waiting", "terminated"]
        
        # Sample a subset of pods for containers
        container_pods = random.sample(pods, min(len(pods), 50))
        
        for pod in container_pods:
            # Each pod typically has 1-3 containers
            containers_in_pod = random.randint(1, 3)
            for container_num in range(1, containers_in_pod + 1):
                image = random.choice(images)
                container = Container(
                    id=self.generate_id("ctr"),
                    name=f"{pod.name}-container-{container_num}",
                    image=image.split(':')[0],
                    image_tag=image.split(':')[1] if ':' in image else "latest",
                    container_id=self.generate_id("cid"),
                    ports=[f"{random.randint(3000, 9000)}", f"{random.randint(8000, 9000)}"],
                    cpu_limit=f"{random.randint(100, 2000)}m",
                    memory_limit=f"{random.randint(128, 4096)}Mi",
                    status=random.choice(statuses)
                )
                
                # Set environment variables using the new method
                container.set_environment_vars({
                    "ENV": random.choice(["production", "staging", "development"]),
                    "LOG_LEVEL": random.choice(["INFO", "DEBUG", "WARN"]),
                    "MAX_CONNECTIONS": str(random.randint(100, 1000))
                })
                containers.append(container)
                self.entities.append(container)
                
                # Create relationship: Pod -> Container
                rel = Relationship(
                    source_id=pod.id,
                    target_id=container.id,
                    relationship_type=RelationshipType.CONTAINS
                )
                rel.set_properties({"image": container.image, "status": container.status})
                self.relationships.append(rel)
        
        return containers
    
    def create_network_relationships(self, ports: List[NetworkPort], vlans: List[VLAN], servers: List[Server]):
        """Create network connectivity relationships"""
        # Connect ports to VLANs
        for port in random.sample(ports, min(len(ports), len(vlans) * 3)):
            vlan = random.choice(vlans)
            rel = Relationship(
                source_id=port.id,
                target_id=vlan.id,
                relationship_type=RelationshipType.BELONGS_TO
            )
            rel.set_properties({"access_type": random.choice(["access", "trunk"])})
            self.relationships.append(rel)
        
        # Connect servers to VLANs
        for server in servers:
            vlan = random.choice(vlans)
            rel = Relationship(
                source_id=server.id,
                target_id=vlan.id,
                relationship_type=RelationshipType.CONNECTED_TO
            )
            rel.set_properties({"interface": "eth0"})
            self.relationships.append(rel)
    
    def generate_full_topology(self) -> Tuple[List, List]:
        """Generate complete network topology"""
        print("🏗️  Generating network infrastructure topology...")
        
        # Create infrastructure components
        switches = self.create_network_switches(3)
        ports = self.create_network_ports(switches, 24)
        vlans = self.create_vlans(10)
        servers = self.create_servers(5)
        vms = self.create_virtual_machines(servers, 10)
        pods = self.create_kubernetes_pods(vms, 100)
        containers = self.create_containers(pods, 1000)
        
        # Create network relationships
        self.create_network_relationships(ports, vlans, servers)
        
        print(f"✅ Generated topology with:")
        print(f"   - {len(switches)} network switches")
        print(f"   - {len(ports)} network ports")
        print(f"   - {len(vlans)} VLANs")
        print(f"   - {len(servers)} servers")
        print(f"   - {len(vms)} virtual machines")
        print(f"   - {len(pods)} Kubernetes pods")
        print(f"   - {len(containers)} containers")
        print(f"   - {len(self.relationships)} relationships")
        
        return self.entities, self.relationships
    
    def populate_database(self):
        """Generate and populate the database with sample data"""
        entities, relationships = self.generate_full_topology()
        
        print("\n📊 Populating Neo4j database...")
        
        # Create entities
        for entity in entities:
            self.kg.create_entity(entity)
        
        # Create relationships
        for relationship in relationships:
            self.kg.create_relationship(relationship)
        
        print(f"\n✅ Database populated successfully!")
        
        # Print statistics
        stats = self.kg.get_statistics()
        print(f"\n📈 Database Statistics:")
        print(f"   Total entities: {stats['total_entities']}")
        print(f"   Total relationships: {stats['total_relationships']}")
        print(f"   Entity breakdown: {stats['entity_counts']}")
        print(f"   Relationship breakdown: {stats['relationship_counts']}")


if __name__ == "__main__":
    # Example usage
    kg = Neo4jKnowledgeGraph()
    generator = InfrastructureDataGenerator(kg)
    
    # Setup database
    kg.setup_constraints_and_indexes()
    
    # Generate and populate data
    generator.populate_database()
    
    kg.close() 