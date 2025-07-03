# =============================================================================
# DATA_GENERATOR.PY - SAMPLE DATA GENERATOR FOR NETWORK INFRASTRUCTURE TOPOLOGY
# =============================================================================
# This file creates realistic sample network infrastructure data for testing and demonstration
# Think of it as a "network builder simulator" that creates a virtual data center
#
# WHAT DOES THIS FILE DO?
# This file generates realistic sample data that represents a real network infrastructure:
# - Network switches with multiple ports
# - VLANs (network segments) for organizing traffic
# - Physical servers with realistic specifications
# - Virtual machines running on those servers
# - Kubernetes pods containing applications
# - Containers running inside the pods
# - All the relationships connecting these components
#
# WHY DO WE NEED SAMPLE DATA?
# 1. Testing: We need data to test our knowledge graph system
# 2. Demonstration: Sample data shows how the system works with realistic scenarios
# 3. Development: Developers need consistent data to build and test features
# 4. Training: AI/LLM systems need example data to learn from
#
# HOW DOES DATA GENERATION WORK?
# The generator follows the real-world hierarchy of network infrastructure:
# Switch → Ports → VLANs → Servers → VMs → Pods → Containers
# Each layer builds upon the previous layer, creating realistic relationships

# DOCSTRING - Documentation that explains what this file contains
# =============================================================================
"""
Sample data generator for network infrastructure topology

This module creates realistic sample data representing a complete network
infrastructure topology. It generates:

1. Network Layer: Switches, ports, and VLANs
2. Compute Layer: Physical servers and virtual machines  
3. Application Layer: Kubernetes pods and containers
4. Relationships: All the connections between these components

The generated data follows real-world patterns and constraints:
- Switches have a realistic number of ports (24, 48, etc.)
- Servers have appropriate CPU, memory, and storage specifications
- VMs are properly allocated within server resource limits
- Pods and containers follow Kubernetes naming conventions
- IP addresses follow standard networking patterns

This data is used for testing, demonstration, and training purposes.
"""

# IMPORT STATEMENTS - Getting tools we need from other Python libraries
# =============================================================================

# random: For generating random numbers and making random choices
# This is essential for creating varied, realistic sample data
import random

# string: For working with text characters (letters, numbers, symbols)
# We use this to generate random IDs and network addresses
import string

# typing: For specifying what types of data our functions expect and return
# This helps catch errors and makes code more readable
from typing import List, Tuple

# datetime: For working with dates and times
# We use this to timestamp when entities were created
from datetime import datetime

# Import our data models - the "blueprints" for network entities
# These define what information each type of network component needs
from .models import (
    NetworkSwitch, NetworkPort, VLAN, Server, VirtualMachine,
    KubernetesPod, Container, Relationship, RelationshipType
)

# Import our database interface for storing the generated data
from .database import Neo4jKnowledgeGraph


# MAIN DATA GENERATOR CLASS - The "network builder simulator"
# =============================================================================

class InfrastructureDataGenerator:
    """
    Generate sample network infrastructure data
    
    WHAT IS THIS CLASS?
    This class is like a "virtual network architect" that designs and builds
    a complete network infrastructure from scratch. It creates all the components
    you'd find in a real data center and connects them properly.
    
    HOW DOES IT WORK?
    1. Creates the foundation (switches and network infrastructure)
    2. Builds the compute layer (servers and virtual machines)
    3. Adds the application layer (Kubernetes pods and containers)
    4. Connects everything with realistic relationships
    5. Stores all the data in the Neo4j database
    
    OBJECT-ORIENTED PROGRAMMING CONCEPT:
    This class encapsulates (bundles together) all the data generation logic
    It keeps track of all the entities and relationships it creates
    """
    
    def __init__(self, kg: Neo4jKnowledgeGraph):
        """
        Initialize the data generator
        
        WHAT IS __init__?
        This is the constructor - it sets up the data generator when it's first created
        Think of it like preparing a construction site before building
        
        PARAMETERS:
        kg: Neo4jKnowledgeGraph - The database connection where we'll store the generated data
        
        WHAT GETS INITIALIZED?
        - A reference to the knowledge graph database
        - Empty lists to track entities and relationships we create
        """
        # Store the database connection so we can use it throughout the class
        self.kg = kg
        
        # Initialize empty lists to keep track of what we create
        # entities: All the network components (switches, servers, VMs, etc.)
        self.entities = []
        
        # relationships: All the connections between components
        self.relationships = []
    
    # UTILITY METHODS - Helper functions for generating realistic data
    # -------------------------------------------------------------------------
    
    def generate_id(self, prefix: str) -> str:
        """
        Generate a unique ID with prefix
        
        WHAT DOES THIS DO?
        Creates unique identifiers for network components
        For example: "sw-a7b3f2k1", "srv-x9z4m8n2", "vm-q5w7e1r3"
        
        WHY USE PREFIXES?
        - "sw" for switches, "srv" for servers, "vm" for virtual machines
        - Makes it easy to identify what type of component an ID refers to
        - Helps with debugging and troubleshooting
        
        HOW IT WORKS:
        1. Takes a prefix (like "sw" for switch)
        2. Generates 8 random characters (letters and numbers)
        3. Combines them with a dash: "sw-a7b3f2k1"
        """
        # Generate 8 random characters from lowercase letters and digits
        # ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
        # digits = '0123456789'
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        
        # Combine prefix with random suffix using a dash
        return f"{prefix}-{random_suffix}"
    
    def generate_ip_address(self, subnet: str = "10.0") -> str:
        """
        Generate a random IP address
        
        WHAT IS AN IP ADDRESS?
        An IP address is like a "street address" for network devices
        It tells other devices how to find and communicate with a specific device
        Format: 192.168.1.100 (four numbers separated by dots)
        
        PARAMETERS:
        subnet: str - The first part of the IP address (default "10.0")
        
        HOW IT WORKS:
        1. Takes a subnet prefix (like "10.0")
        2. Generates two random numbers between 1 and 254
        3. Combines them: "10.0.45.123"
        
        WHY 1-254?
        - 0 is reserved for network address
        - 255 is reserved for broadcast address
        - 1-254 are valid host addresses
        """
        # Generate two random numbers for the last two octets of the IP
        third_octet = random.randint(1, 254)
        fourth_octet = random.randint(1, 254)
        
        # Combine with the subnet prefix
        return f"{subnet}.{third_octet}.{fourth_octet}"
    
    def generate_mac_address(self) -> str:
        """
        Generate a random MAC address
        
        WHAT IS A MAC ADDRESS?
        A MAC address is like a "fingerprint" for network hardware
        Every network card has a unique MAC address burned into it
        Format: 00:1B:44:11:3A:B7 (six pairs of hexadecimal numbers)
        
        HOW IT WORKS:
        1. Generates 6 random numbers (0-255)
        2. Converts each to hexadecimal format (00-FF)
        3. Joins them with colons: "a4:5e:60:c2:8f:1d"
        """
        # Generate 6 random bytes and format them as hexadecimal
        mac_parts = []
        for _ in range(6):
            # Generate random number 0-255, format as 2-digit hex (lowercase)
            part = f"{random.randint(0, 255):02x}"
            mac_parts.append(part)
        
        # Join with colons to create standard MAC address format
        return ":".join(mac_parts)
    
    # NETWORK LAYER GENERATION - Creating switches, ports, and VLANs
    # -------------------------------------------------------------------------
    
    def create_network_switches(self, count: int = 3) -> List[NetworkSwitch]:
        """
        Create network switches
        
        WHAT ARE NETWORK SWITCHES?
        Network switches are like "digital traffic directors" for network traffic
        They connect multiple devices and forward data between them
        Think of them like the electrical panel in a building that distributes power
        
        PARAMETERS:
        count: int - How many switches to create (default 3)
        
        RETURN VALUE:
        List[NetworkSwitch] - A list of switch objects
        
        REALISTIC DATA PATTERNS:
        - Uses real network equipment vendors (Cisco, Juniper, etc.)
        - Uses realistic switch models and port counts
        - Assigns switches to different data center locations
        """
        switches = []
        
        # Lists of realistic data for generating varied switches
        # These are based on real network equipment vendors and models
        vendors = ["Cisco", "Juniper", "Arista", "HP", "Dell"]
        models = ["Catalyst 9300", "EX4300", "7050X", "ProCurve 2920", "PowerSwitch S3048"]
        locations = ["DataCenter-A", "DataCenter-B", "Edge-01", "Core-01", "Dist-01"]
        
        # Create the specified number of switches
        for i in range(count):
            # Create a switch with realistic specifications
            switch = NetworkSwitch(
                id=self.generate_id("sw"),                    # Unique ID like "sw-a7b3f2k1"
                name=f"Switch-{i+1:02d}",                     # Human-readable name like "Switch-01"
                vendor=random.choice(vendors),                # Random vendor from our list
                model=random.choice(models),                  # Random model from our list
                ip_address=self.generate_ip_address("192.168.1"),  # Management IP for the switch
                mac_address=self.generate_mac_address(),      # Unique hardware address
                port_count=random.choice([24, 48, 72]),       # Realistic port counts
                location=random.choice(locations)             # Random data center location
            )
            
            # Add the switch to our collections
            switches.append(switch)          # Add to local list for return
            self.entities.append(switch)     # Add to master entity list
        
        return switches
    
    def create_network_ports(self, switches: List[NetworkSwitch], ports_per_switch: int = 24) -> List[NetworkPort]:
        """
        Create network ports for switches
        
        WHAT ARE NETWORK PORTS?
        Network ports are the individual connection points on a switch
        Think of them like electrical outlets on a power strip
        Each port can connect to one device (server, computer, another switch, etc.)
        
        PARAMETERS:
        switches: List[NetworkSwitch] - The switches to create ports for
        ports_per_switch: int - How many ports each switch should have
        
        RETURN VALUE:
        List[NetworkPort] - A list of all created ports
        
        REALISTIC PATTERNS:
        - Different port types (Gigabit, 10-Gigabit, etc.)
        - Realistic speeds and duplex settings
        - Some ports may be down (realistic operational status)
        """
        ports = []
        
        # Realistic port types found on network switches
        port_types = ["GigabitEthernet", "TenGigabitEthernet", "FastEthernet"]
        
        # Create ports for each switch
        for switch in switches:
            # Create the specified number of ports for this switch
            for port_num in range(1, ports_per_switch + 1):
                # Create a port with realistic specifications
                port = NetworkPort(
                    id=self.generate_id("port"),                        # Unique ID
                    name=f"{switch.name}-Port-{port_num:02d}",           # Descriptive name
                    port_number=port_num,                               # Physical port number
                    port_type=random.choice(port_types),                # Random port type
                    status=random.choice(["up", "down"]),               # Operational status
                    speed=random.choice(["1000Mbps", "100Mbps", "10Gbps"]),  # Port speed
                    duplex=random.choice(["full", "half"])              # Duplex mode
                )
                
                # Add the port to our collections
                ports.append(port)
                self.entities.append(port)
                
                # Create the relationship: Switch CONTAINS Port
                # This represents the physical connection between switch and port
                rel = Relationship(
                    source_id=switch.id,                               # The switch
                    target_id=port.id,                                 # The port
                    relationship_type=RelationshipType.CONTAINS        # Relationship type
                )
                
                # Add additional properties to the relationship
                rel.set_properties({"port_number": port_num})
                self.relationships.append(rel)
        
        return ports
    
    def create_vlans(self, count: int = 10) -> List[VLAN]:
        """
        Create VLANs (Virtual Local Area Networks)
        
        WHAT ARE VLANs?
        VLANs are like "virtual roads" on the same physical network
        They separate different types of traffic for security and performance
        For example: one VLAN for office computers, another for printers
        
        PARAMETERS:
        count: int - How many VLANs to create (default 10)
        
        RETURN VALUE:
        List[VLAN] - A list of VLAN objects
        
        REALISTIC PATTERNS:
        - Common VLAN names used in real networks
        - Valid VLAN ID ranges (10-4094)
        - Proper subnet addressing schemes
        """
        vlans = []
        
        # Common VLAN names used in real network environments
        vlan_names = [
            "Management",    # For network management traffic
            "Production",    # For production application servers
            "Development",   # For development and testing
            "DMZ",          # For publicly accessible services
            "Guest",        # For guest user access
            "Storage",      # For storage area network traffic
            "Backup",       # For backup operations
            "Security",     # For security appliances
            "IoT",          # For Internet of Things devices
            "Voice"         # For VoIP phone systems
        ]
        
        # Create VLANs using the names (up to the requested count)
        for i, name in enumerate(vlan_names[:count]):
            # Generate a random VLAN ID (10-4094 is the valid range)
            vlan_id = random.randint(10, 4094)
            
            # Create a VLAN with realistic network addressing
            vlan = VLAN(
                id=self.generate_id("vlan"),                           # Unique ID
                name=f"VLAN-{name}",                                   # Descriptive name
                vlan_id=vlan_id,                                       # VLAN number
                subnet=f"10.{vlan_id//100}.{vlan_id%100}.0/24",        # IP subnet
                gateway=f"10.{vlan_id//100}.{vlan_id%100}.1",          # Gateway IP
                description=f"{name} VLAN"                             # Description
            )
            
            # Add the VLAN to our collections
            vlans.append(vlan)
            self.entities.append(vlan)
        
        return vlans
    
    # COMPUTE LAYER GENERATION - Creating servers and virtual machines
    # -------------------------------------------------------------------------
    
    def create_servers(self, count: int = 5) -> List[Server]:
        """
        Create physical servers
        
        WHAT ARE SERVERS?
        Servers are powerful computers that provide services to other computers
        They're like "workhorses" that do the heavy computing in a data center
        They typically run multiple virtual machines or applications
        
        PARAMETERS:
        count: int - How many servers to create (default 5)
        
        RETURN VALUE:
        List[Server] - A list of server objects
        
        REALISTIC PATTERNS:
        - Enterprise-grade hardware specifications
        - Common server operating systems
        - Realistic rack locations in data centers
        """
        servers = []
        
        # Common operating systems used on servers
        os_types = [
            "Ubuntu 20.04",        # Popular Linux distribution
            "RHEL 8",              # Red Hat Enterprise Linux
            "CentOS 7",            # Community Enterprise OS
            "Windows Server 2019", # Microsoft server OS
            "VMware ESXi 7.0"      # Virtualization hypervisor
        ]
        
        # Create the specified number of servers
        for i in range(count):
            # Create a server with enterprise-grade specifications
            server = Server(
                id=self.generate_id("srv"),                            # Unique ID
                name=f"Server-{i+1:02d}",                              # Human-readable name
                hostname=f"srv-{i+1:02d}.example.com",                 # Full domain name
                ip_address=self.generate_ip_address("10.1"),           # Server IP address
                mac_address=self.generate_mac_address(),               # Hardware address
                cpu_cores=random.choice([16, 32, 64, 128]),            # Enterprise CPU counts
                memory_gb=random.choice([64, 128, 256, 512]),          # Enterprise memory amounts
                storage_gb=random.choice([1000, 2000, 4000, 8000]),    # Enterprise storage capacity
                os=random.choice(os_types),                            # Random OS
                rack_location=f"Rack-{random.randint(1, 20)}-U{random.randint(1, 42)}"  # Data center location
            )
            
            # Add the server to our collections
            servers.append(server)
            self.entities.append(server)
        
        return servers
    
    def create_virtual_machines(self, servers: List[Server], vms_per_server: int = 10) -> List[VirtualMachine]:
        """
        Create virtual machines on servers
        
        WHAT ARE VIRTUAL MACHINES?
        Virtual machines are like "computers within computers"
        One physical server can run many virtual machines simultaneously
        Each VM acts like an independent computer with its own OS and applications
        
        PARAMETERS:
        servers: List[Server] - The physical servers to host VMs
        vms_per_server: int - How many VMs each server should host
        
        RETURN VALUE:
        List[VirtualMachine] - A list of virtual machine objects
        
        REALISTIC PATTERNS:
        - VM resources are smaller than host server resources
        - Common guest operating systems
        - Various hypervisor platforms
        """
        vms = []
        
        # Common operating systems used in virtual machines
        vm_os_types = [
            "Ubuntu 20.04",       # Popular Linux for applications
            "Ubuntu 22.04",       # Newer Ubuntu version
            "CentOS 8",           # Enterprise Linux
            "Windows 10",         # Desktop OS in enterprise
            "Windows Server 2019" # Server OS for Windows applications
        ]
        
        # Hypervisor platforms used for virtualization
        hypervisors = [
            "VMware vSphere",     # Enterprise virtualization platform
            "KVM",                # Open-source Linux hypervisor
            "Hyper-V",            # Microsoft virtualization
            "Xen"                 # Open-source hypervisor
        ]
        
        # Create VMs for each server
        for server in servers:
            # Create the specified number of VMs per server
            for vm_num in range(1, vms_per_server + 1):
                # Create a VM with resources appropriate for a virtual machine
                vm = VirtualMachine(
                    id=self.generate_id("vm"),                         # Unique ID
                    name=f"{server.name}-VM-{vm_num:02d}",              # Descriptive name
                    hostname=f"vm-{server.name.lower()}-{vm_num:02d}.example.com",  # Full domain name
                    ip_address=self.generate_ip_address("10.2"),       # VM IP address
                    cpu_cores=random.choice([2, 4, 8, 16]),            # VM CPU allocation
                    memory_gb=random.choice([4, 8, 16, 32]),           # VM memory allocation
                    storage_gb=random.choice([50, 100, 200, 500]),     # VM storage allocation
                    os=random.choice(vm_os_types),                     # Guest OS
                    hypervisor=random.choice(hypervisors),             # Virtualization platform
                    vm_id=self.generate_id("vmid")                     # Hypervisor-specific ID
                )
                
                # Add the VM to our collections
                vms.append(vm)
                self.entities.append(vm)
                
                # Create the relationship: Server HOSTS VirtualMachine
                # This represents the physical server providing resources to the VM
                rel = Relationship(
                    source_id=server.id,                               # The physical server
                    target_id=vm.id,                                   # The virtual machine
                    relationship_type=RelationshipType.HOSTS           # Relationship type
                )
                
                # Add additional properties to the relationship
                rel.set_properties({"hypervisor": vm.hypervisor})
                self.relationships.append(rel)
        
        return vms
    
    # APPLICATION LAYER GENERATION - Creating Kubernetes pods and containers
    # -------------------------------------------------------------------------
    
    def create_kubernetes_pods(self, vms: List[VirtualMachine], pods_per_vm: int = 100) -> List[KubernetesPod]:
        """
        Create Kubernetes pods on VMs
        
        WHAT ARE KUBERNETES PODS?
        Kubernetes pods are like "shipping containers" for applications
        They're the smallest unit in Kubernetes that can contain one or more containers
        Pods provide shared networking and storage for their containers
        
        PARAMETERS:
        vms: List[VirtualMachine] - The VMs that will run Kubernetes
        pods_per_vm: int - How many pods each Kubernetes VM should run
        
        RETURN VALUE:
        List[KubernetesPod] - A list of Kubernetes pod objects
        
        REALISTIC PATTERNS:
        - Common Kubernetes namespaces for organizing applications
        - Realistic pod lifecycle phases
        - Kubernetes-style naming conventions
        - Labels and annotations used for metadata
        """
        pods = []
        
        # Common Kubernetes namespaces for organizing applications
        namespaces = [
            "default",        # Default namespace
            "kube-system",    # System components
            "production",     # Production applications
            "staging",        # Staging environment
            "development",    # Development environment
            "monitoring",     # Monitoring tools
            "logging"         # Logging infrastructure
        ]
        
        # Kubernetes pod lifecycle phases
        phases = [
            "Running",        # Pod is running successfully
            "Pending",        # Pod is being scheduled
            "Succeeded",      # Pod completed successfully
            "Failed",         # Pod failed to run
            "Unknown"         # Pod status is unknown
        ]
        
        # Only create pods on some VMs (those that would be Kubernetes nodes)
        # In reality, not every VM runs Kubernetes
        k8s_vms = random.sample(vms, min(len(vms), 3))
        
        # Create pods for each Kubernetes VM
        for vm in k8s_vms:
            # Create the specified number of pods per VM
            for pod_num in range(1, pods_per_vm + 1):
                # Choose a random namespace for this pod
                namespace = random.choice(namespaces)
                
                # Create a pod with Kubernetes-appropriate specifications
                pod = KubernetesPod(
                    id=self.generate_id("pod"),                        # Unique ID
                    name=f"pod-{namespace}-{pod_num:03d}",              # Kubernetes naming convention
                    namespace=namespace,                               # Kubernetes namespace
                    pod_ip=self.generate_ip_address("10.244"),          # Pod network IP
                    node_name=vm.hostname,                             # Kubernetes node (VM)
                    phase=random.choice(phases),                       # Pod lifecycle phase
                    restart_count=random.randint(0, 10)                # How many times restarted
                )
                
                # Set Kubernetes labels (metadata for organizing and selecting pods)
                pod.set_k8s_labels({
                    "app": f"app-{random.randint(1, 10)}",             # Application name
                    "version": f"v{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}",  # Version
                    "environment": random.choice(["prod", "staging", "dev"])  # Environment type
                })
                
                # Set Kubernetes annotations (additional metadata)
                pod.set_annotations({
                    "created-by": "deployment-controller",             # What created this pod
                    "last-restart": datetime.now().isoformat()         # When it was last restarted
                })
                
                # Add the pod to our collections
                pods.append(pod)
                self.entities.append(pod)
                
                # Create the relationship: VirtualMachine HOSTS KubernetesPod
                # This represents the VM providing resources to run the pod
                rel = Relationship(
                    source_id=vm.id,                                   # The virtual machine
                    target_id=pod.id,                                  # The Kubernetes pod
                    relationship_type=RelationshipType.HOSTS           # Relationship type
                )
                
                # Add additional properties to the relationship
                rel.set_properties({
                    "namespace": namespace,
                    "node_name": vm.hostname
                })
                self.relationships.append(rel)
        
        return pods
    
    def create_containers(self, pods: List[KubernetesPod], containers_per_pod: int = 1000) -> List[Container]:
        """
        Create containers inside pods
        
        WHAT ARE CONTAINERS?
        Containers are like "shipping containers" for applications
        They package an application with all its dependencies
        Multiple containers can run on the same machine but stay isolated
        
        PARAMETERS:
        pods: List[KubernetesPod] - The pods that will contain containers
        containers_per_pod: int - How many containers to create total (distributed across pods)
        
        RETURN VALUE:
        List[Container] - A list of container objects
        
        REALISTIC PATTERNS:
        - Common container images (nginx, redis, postgres, etc.)
        - Realistic resource limits and port configurations
        - Container environment variables
        """
        containers = []
        
        # Common container images used in production environments
        images = [
            "nginx",              # Web server
            "redis",              # In-memory database
            "postgres",           # SQL database
            "mysql",              # SQL database
            "mongodb",            # NoSQL database
            "node",               # Node.js runtime
            "python",             # Python runtime
            "openjdk",            # Java runtime
            "alpine",             # Minimal Linux base image
            "ubuntu"              # Ubuntu base image
        ]
        
        # Common image tags (versions)
        tags = ["latest", "stable", "alpine", "1.0", "2.1", "3.6"]
        
        # Container statuses
        statuses = ["running", "stopped", "created", "restarting", "removing"]
        
        # Create containers distributed across pods
        # We'll create fewer containers per pod than the total requested
        containers_created = 0
        
        for pod in pods:
            # Create 1-3 containers per pod (realistic for most applications)
            containers_in_pod = random.randint(1, 3)
            
            for container_num in range(containers_in_pod):
                if containers_created >= containers_per_pod:
                    break
                
                # Choose random image and tag
                image = random.choice(images)
                tag = random.choice(tags)
                
                # Create a container with realistic specifications
                container = Container(
                    id=self.generate_id("cont"),                       # Unique ID
                    name=f"{pod.name}-{image}-{container_num}",         # Descriptive name
                    image=f"{image}:{tag}",                            # Container image with tag
                    image_tag=tag,                                     # Image version tag
                    container_id=self.generate_id("cid"),              # Runtime container ID
                    ports=[f"{random.randint(3000, 9000)}"],           # Exposed ports
                    cpu_limit=f"{random.choice([0.1, 0.5, 1.0, 2.0])}", # CPU resource limit
                    memory_limit=f"{random.choice([128, 256, 512, 1024])}Mi", # Memory limit
                    status=random.choice(statuses)                     # Container status
                )
                
                # Set environment variables (configuration for the container)
                container.set_environment_vars({
                    "NODE_ENV": random.choice(["production", "development", "staging"]),
                    "PORT": str(random.randint(3000, 9000)),
                    "LOG_LEVEL": random.choice(["info", "debug", "warn", "error"])
                })
                
                # Add the container to our collections
                containers.append(container)
                self.entities.append(container)
                containers_created += 1
                
                # Create the relationship: KubernetesPod CONTAINS Container
                # This represents the pod providing the execution environment for the container
                rel = Relationship(
                    source_id=pod.id,                                  # The Kubernetes pod
                    target_id=container.id,                            # The container
                    relationship_type=RelationshipType.CONTAINS        # Relationship type
                )
                
                # Add additional properties to the relationship
                rel.set_properties({
                    "image": container.image,
                    "status": container.status
                })
                self.relationships.append(rel)
            
            if containers_created >= containers_per_pod:
                break
        
        return containers
    
    # NETWORK RELATIONSHIP GENERATION - Connecting components to network infrastructure
    # -------------------------------------------------------------------------
    
    def create_network_relationships(self, ports: List[NetworkPort], vlans: List[VLAN], servers: List[Server]):
        """
        Create relationships between network components
        
        WHAT DOES THIS DO?
        This method creates the "network wiring" that connects everything together
        It simulates how servers connect to switch ports and how VLANs organize traffic
        
        PARAMETERS:
        ports: List[NetworkPort] - Available switch ports
        vlans: List[VLAN] - Available VLANs for organizing traffic
        servers: List[Server] - Servers that need network connections
        
        REALISTIC PATTERNS:
        - Servers connect to switch ports (physical connections)
        - Ports belong to VLANs (logical network segments)
        - Not all ports are used (realistic port utilization)
        """
        # Connect servers to switch ports
        # In reality, each server connects to one or more switch ports
        available_ports = [port for port in ports if port.status == "up"]  # Only use active ports
        
        for server in servers:
            if available_ports:  # Make sure we have ports available
                # Connect server to a random available port
                port = random.choice(available_ports)
                available_ports.remove(port)  # Remove from available list
                
                # Create the relationship: Server CONNECTED_TO NetworkPort
                rel = Relationship(
                    source_id=server.id,                               # The server
                    target_id=port.id,                                 # The network port
                    relationship_type=RelationshipType.CONNECTED_TO    # Relationship type
                )
                
                # Add additional properties to the relationship
                rel.set_properties({
                    "connection_type": "primary",
                    "speed": port.speed
                })
                self.relationships.append(rel)
        
        # Assign ports to VLANs
        # In reality, network ports are configured to carry traffic for specific VLANs
        for port in ports:
            if random.random() < 0.8:  # 80% of ports are assigned to VLANs
                vlan = random.choice(vlans)
                
                # Create the relationship: NetworkPort BELONGS_TO VLAN
                rel = Relationship(
                    source_id=port.id,                                 # The network port
                    target_id=vlan.id,                                 # The VLAN
                    relationship_type=RelationshipType.BELONGS_TO      # Relationship type
                )
                
                # Add additional properties to the relationship
                rel.set_properties({
                    "access_mode": random.choice(["access", "trunk"]),  # VLAN configuration mode
                    "native_vlan": random.choice([True, False])        # Whether this is the native VLAN
                })
                self.relationships.append(rel)
    
    # TOPOLOGY GENERATION ORCHESTRATION - Coordinating all the data generation
    # -------------------------------------------------------------------------
    
    def generate_full_topology(self) -> Tuple[List, List]:
        """
        Generate a complete network infrastructure topology
        
        WHAT DOES THIS DO?
        This is the "master conductor" that orchestrates the creation of an entire
        network infrastructure. It creates all components and their relationships
        in the correct order.
        
        RETURN VALUE:
        Tuple[List, List] - A tuple containing (entities, relationships)
        
        GENERATION ORDER:
        1. Network layer (switches, ports, VLANs)
        2. Compute layer (servers, VMs)
        3. Application layer (pods, containers)
        4. Network relationships (connections)
        """
        print("🏗️  Generating network infrastructure topology...")
        
        # Step 1: Create network infrastructure foundation
        print("   📡 Creating network switches...")
        switches = self.create_network_switches(count=3)
        
        print("   🔌 Creating network ports...")
        ports = self.create_network_ports(switches, ports_per_switch=24)
        
        print("   🏷️  Creating VLANs...")
        vlans = self.create_vlans(count=10)
        
        # Step 2: Create compute infrastructure
        print("   🖥️  Creating physical servers...")
        servers = self.create_servers(count=5)
        
        print("   💻 Creating virtual machines...")
        vms = self.create_virtual_machines(servers, vms_per_server=10)
        
        # Step 3: Create application infrastructure
        print("   🚀 Creating Kubernetes pods...")
        pods = self.create_kubernetes_pods(vms, pods_per_vm=100)
        
        print("   📦 Creating containers...")
        containers = self.create_containers(pods, containers_per_pod=100)
        
        # Step 4: Create network relationships
        print("   🔗 Creating network relationships...")
        self.create_network_relationships(ports, vlans, servers)
        
        # Return all generated entities and relationships
        return self.entities, self.relationships
    
    def populate_database(self):
        """
        Generate topology and populate the Neo4j database
        
        WHAT DOES THIS DO?
        This is the "final step" that takes all the generated data and stores it
        in the Neo4j database. It's like moving from the blueprint to the actual building.
        
        PROCESS:
        1. Generate all entities and relationships
        2. Store each entity in the database
        3. Store each relationship in the database
        4. Report statistics about what was created
        """
        print("\n🚀 Starting database population...")
        
        # Generate the complete topology
        entities, relationships = self.generate_full_topology()
        
        # Store all entities in the database
        print(f"\n📊 Storing {len(entities)} entities in database...")
        created_entities = 0
        for entity in entities:
            if self.kg.create_entity(entity):
                created_entities += 1
        
        # Store all relationships in the database
        print(f"🔗 Storing {len(relationships)} relationships in database...")
        created_relationships = 0
        for relationship in relationships:
            if self.kg.create_relationship(relationship):
                created_relationships += 1
        
        # Report final statistics
        print(f"\n✅ Database population completed!")
        print(f"   📊 Entities created: {created_entities}/{len(entities)}")
        print(f"   🔗 Relationships created: {created_relationships}/{len(relationships)}")
        
        # Get and display database statistics
        stats = self.kg.get_statistics()
        print(f"\n📈 Database Statistics:")
        print(f"   Total entities: {stats['total_entities']}")
        print(f"   Total relationships: {stats['total_relationships']}")
        print(f"   Entity breakdown:")
        for entity_type, count in stats['entity_counts'].items():
            print(f"     - {entity_type}: {count}")
        
        print(f"\n🎉 Sample data generation completed successfully!")
        print(f"💡 You can now explore the data using:")
        print(f"   - Neo4j Browser: http://localhost:7474")
        print(f"   - Streamlit Dashboard: streamlit run streamlit_app.py")
        print(f"   - Main Demo: python main.py")


if __name__ == "__main__":
    # Example usage
    kg = Neo4jKnowledgeGraph()
    generator = InfrastructureDataGenerator(kg)
    
    # Setup database
    kg.setup_constraints_and_indexes()
    
    # Generate and populate data
    generator.populate_database()
    
    kg.close() 