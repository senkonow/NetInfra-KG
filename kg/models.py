# =============================================================================
# MODELS.PY - DATA STRUCTURES FOR NETWORK INFRASTRUCTURE ENTITIES
# =============================================================================
# This file defines the "blueprints" for all the different types of network equipment
# Think of it like architectural blueprints that define what a house looks like
# Except these blueprints define what network switches, servers, VMs, etc. look like
#
# WHAT IS A PYDANTIC MODEL?
# Pydantic is a Python library that helps us create "data classes" with validation
# It's like having a "quality control inspector" for our data
# When we create a new server or switch, Pydantic checks that all the information
# is correct (like making sure IP addresses look like real IP addresses)
#
# WHY DO WE NEED THESE MODELS?
# 1. Data Validation: Makes sure our data is correct before storing it
# 2. Type Safety: Helps catch errors before they cause problems
# 3. Documentation: Clearly defines what information each entity needs
# 4. Consistency: Ensures all entities have the same structure

# DOCSTRING - Documentation that explains what this file contains
# =============================================================================
"""
Pydantic models for network infrastructure entities

This file defines the data structures for all the different types of network
equipment and infrastructure components in our knowledge graph:

- NetworkSwitch: Physical network switches that connect devices
- NetworkPort: Individual ports on network switches
- VLAN: Virtual Local Area Networks that segment network traffic
- Server: Physical servers that host virtual machines
- VirtualMachine: Virtual computers running on physical servers
- KubernetesPod: Kubernetes pods that run containerized applications
- Container: Individual containers running applications

Each model defines what information we need to store for each type of entity,
validates that the data is correct, and provides helper methods for working
with the data.
"""

# IMPORT STATEMENTS - Getting tools we need from other Python libraries
# =============================================================================

# typing: Helps us specify what types of data our functions expect
# This is like putting "labels" on our code to make it clearer
from typing import Optional, List, Dict, Any, Literal, Union

# pydantic: The main library for creating data models with validation
# BaseModel: The foundation class that all our models inherit from
# Field: Used to add descriptions and validation rules to our data fields
# validator: Used to create custom validation functions
from pydantic import BaseModel, Field, validator

# datetime: For working with dates and times
# We use this to track when entities were created and updated
from datetime import datetime

# Enum: For creating lists of predefined choices
# This ensures we only use valid values for certain fields
from enum import Enum

# json: For converting between Python dictionaries and JSON strings
# Neo4j can't store complex dictionaries, so we convert them to JSON strings
import json


# ENTITY TYPE ENUMERATION - Predefined list of entity types
# =============================================================================

class EntityType(str, Enum):
    """
    Enumeration of all possible entity types in our network infrastructure
    
    WHAT IS AN ENUMERATION (Enum)?
    An enumeration is like a "multiple choice list" where we define all the
    possible values that are allowed. Think of it like a menu at a restaurant -
    you can only order items that are on the menu.
    
    WHY USE ENUMS?
    1. Prevents typos: Can't accidentally write "NetwokSwitch" instead of "NetworkSwitch"
    2. Provides autocomplete: Your editor can suggest valid values
    3. Makes code more readable: Clear what values are expected
    4. Easier to change: If we need to rename something, we only change it in one place
    
    str, Enum means this enum creates string values that can be used like regular strings
    """
    # Network infrastructure layer - Physical network equipment
    NETWORK_SWITCH = "NetworkSwitch"    # Physical switches that connect devices
    NETWORK_PORT = "NetworkPort"        # Individual ports on switches
    VLAN = "VLAN"                      # Virtual network segments
    
    # Compute layer - Physical and virtual servers
    SERVER = "Server"                   # Physical servers/computers
    VIRTUAL_MACHINE = "VirtualMachine"  # Virtual computers running on servers
    
    # Application layer - Containerized applications
    KUBERNETES_POD = "KubernetesPod"    # Kubernetes pods containing containers
    CONTAINER = "Container"             # Individual application containers


# BASE ENTITY CLASS - The foundation for all network entities
# =============================================================================

class BaseEntity(BaseModel):
    """
    Base model for all network infrastructure entities
    
    WHAT IS A BASE CLASS?
    A base class is like a "foundation" or "template" that other classes build upon
    Think of it like a house foundation - every house needs it, but each house
    can be different on top of the foundation
    
    This BaseEntity class defines the common information that ALL network entities need:
    - A unique ID to identify them
    - A human-readable name
    - When they were created and updated
    - Additional properties for storing custom information
    
    All our specific entity types (NetworkSwitch, Server, etc.) will inherit from this
    base class, meaning they automatically get all these common fields
    """
    
    # COMMON FIELDS - Information that every entity needs
    # -------------------------------------------------------------------------
    
    # id: A unique identifier for this entity
    # Field(..., description="...") creates a field with validation and documentation
    # The "..." means this field is required (cannot be empty)
    id: str = Field(..., description="Unique identifier for this entity")
    
    # name: A human-readable name for this entity
    # This is what people will see when looking at the entity
    name: str = Field(..., description="Human-readable name for this entity")
    
    # type: What type of entity this is (switch, server, VM, etc.)
    # This uses our EntityType enum to ensure only valid types are used
    type: EntityType = Field(..., description="The type of network entity")
    
    # created_at: When this entity was first created
    # default_factory=datetime.now means if no time is provided, use the current time
    created_at: datetime = Field(default_factory=datetime.now, description="When this entity was created")
    
    # updated_at: When this entity was last modified
    updated_at: datetime = Field(default_factory=datetime.now, description="When this entity was last updated")
    
    # properties_json: Additional properties stored as a JSON string
    # WHY JSON STRING INSTEAD OF DICTIONARY?
    # Neo4j database can only store primitive types (strings, numbers, booleans)
    # It cannot store complex dictionaries directly
    # So we convert dictionaries to JSON strings for storage
    properties_json: str = Field(default="{}", description="Additional properties stored as JSON string")
    
    # neo4j_labels: Labels used in Neo4j database
    # Neo4j uses labels to categorize nodes (like tags or categories)
    # default_factory=list creates a new empty list for each entity
    neo4j_labels: List[str] = Field(default_factory=list, description="Labels used in Neo4j database")
    
    # VALIDATORS - Functions that check and clean up our data
    # -------------------------------------------------------------------------
    
    @validator('properties_json', pre=True)
    def serialize_properties(cls, v):
        """
        Validator for properties_json field
        
        WHAT IS A VALIDATOR?
        A validator is like a "quality control inspector" for data
        It checks the data before it gets stored and can modify it if needed
        
        @validator('properties_json', pre=True) means:
        - This function validates the 'properties_json' field
        - pre=True means it runs BEFORE other validation (preprocessing)
        
        WHAT DOES THIS VALIDATOR DO?
        If someone provides a dictionary (dict) for properties, this validator
        automatically converts it to a JSON string using json.dumps()
        
        For example:
        - Input: {"cpu_cores": 8, "memory_gb": 32}
        - Output: '{"cpu_cores": 8, "memory_gb": 32}'
        """
        if isinstance(v, dict):  # If the value is a dictionary
            return json.dumps(v)  # Convert it to a JSON string
        return v  # Otherwise, return the value unchanged
    
    # HELPER METHODS - Functions that make it easier to work with properties
    # -------------------------------------------------------------------------
    
    def set_properties(self, properties: Dict[str, Any]) -> None:
        """
        Set additional properties for this entity
        
        WHAT IS A METHOD?
        A method is a function that belongs to a class
        It's like a "tool" that objects of this class can use
        
        PARAMETERS:
        properties: Dict[str, Any] means a dictionary where:
        - Keys are strings (property names)
        - Values can be anything (str, int, bool, etc.)
        
        -> None means this function doesn't return anything
        It just modifies the object
        
        EXAMPLE USAGE:
        switch = NetworkSwitch(id="SW-001", name="Main Switch")
        switch.set_properties({"cpu_cores": 8, "memory_gb": 32})
        """
        self.properties_json = json.dumps(properties)
    
    def get_properties(self) -> Dict[str, Any]:
        """
        Get additional properties for this entity
        
        RETURN TYPE:
        -> Dict[str, Any] means this function returns a dictionary
        
        This function converts the JSON string back to a Python dictionary
        so it's easier to work with in our code
        
        EXAMPLE USAGE:
        switch = NetworkSwitch(id="SW-001", name="Main Switch")
        switch.set_properties({"cpu_cores": 8, "memory_gb": 32})
        props = switch.get_properties()  # Returns {"cpu_cores": 8, "memory_gb": 32}
        """
        try:
            # Try to parse the JSON string back to a dictionary
            return json.loads(self.properties_json)
        except json.JSONDecodeError:
            # If parsing fails (corrupted JSON), return empty dictionary
            return {}


# NETWORK SWITCH CLASS - Represents physical network switches
# =============================================================================

class NetworkSwitch(BaseEntity):
    """
    Network Switch model
    
    WHAT IS A NETWORK SWITCH?
    A network switch is a physical device that connects multiple devices together
    Think of it like a power strip, but for network connections
    It has multiple ports where you can plug in cables to connect computers,
    servers, and other network devices
    
    WHAT IS CLASS INHERITANCE?
    NetworkSwitch(BaseEntity) means NetworkSwitch inherits from BaseEntity
    This means it automatically gets all the fields from BaseEntity
    (id, name, type, created_at, etc.) plus its own specific fields
    
    It's like inheriting traits from your parents - you get their basic features
    plus your own unique characteristics
    """
    
    # TYPE FIELD - Ensures this entity is always marked as a network switch
    # Literal[EntityType.NETWORK_SWITCH] means this field can ONLY have one value
    # This prevents someone from accidentally creating a switch with the wrong type
    type: Literal[EntityType.NETWORK_SWITCH] = EntityType.NETWORK_SWITCH
    
    # SWITCH-SPECIFIC FIELDS - Information specific to network switches
    # -------------------------------------------------------------------------
    
    # model: The specific model/version of this switch
    # Optional[str] means this field can be a string or None (not required)
    model: Optional[str] = Field(None, description="Switch model (e.g., 'Cisco Catalyst 2960-X')")
    
    # vendor: The manufacturer of this switch
    vendor: Optional[str] = Field(None, description="Switch vendor/manufacturer (e.g., 'Cisco', 'Juniper')")
    
    # ip_address: The IP address used to manage this switch
    # Network administrators use this to connect to the switch for configuration
    ip_address: Optional[str] = Field(None, description="Management IP address for switch administration")
    
    # mac_address: The unique hardware address of this switch
    # Every network device has a unique MAC address (like a fingerprint)
    mac_address: Optional[str] = Field(None, description="MAC address (unique hardware identifier)")
    
    # port_count: How many network ports this switch has
    # Typical switches have 24 or 48 ports
    port_count: Optional[int] = Field(None, description="Number of network ports on this switch")
    
    # location: Where this switch is physically located
    # Helps technicians find the switch when they need to work on it
    location: Optional[str] = Field(None, description="Physical location (e.g., 'Rack 15, Data Center A')")


# NETWORK PORT CLASS - Represents individual ports on network switches
# =============================================================================

class NetworkPort(BaseEntity):
    """
    Network Port model
    
    WHAT IS A NETWORK PORT?
    A network port is an individual connection point on a network switch
    Think of it like a single electrical outlet on a power strip
    Each port can connect to one device (computer, server, another switch, etc.)
    
    Network ports have properties like:
    - Port number (which physical port it is)
    - Speed (how fast data can flow through it)
    - Status (whether it's currently connected and working)
    """
    
    # TYPE FIELD - Ensures this entity is always marked as a network port
    type: Literal[EntityType.NETWORK_PORT] = EntityType.NETWORK_PORT
    
    # PORT-SPECIFIC FIELDS - Information specific to network ports
    # -------------------------------------------------------------------------
    
    # port_number: Which physical port this is on the switch
    # This is required (not Optional) because every port must have a number
    port_number: int = Field(..., description="Physical port number on the switch (e.g., 1, 2, 3...)")
    
    # port_type: What type of port this is
    # Different types support different speeds and cable types
    port_type: Optional[str] = Field(None, description="Port type (e.g., 'FastEthernet', 'GigabitEthernet', 'SFP+')")
    
    # status: Whether this port is currently working
    # Common values: "up" (working), "down" (not connected), "disabled" (turned off)
    status: Optional[str] = Field(None, description="Current port status (e.g., 'up', 'down', 'disabled')")
    
    # speed: How fast data can flow through this port
    # Common values: "100Mbps", "1Gbps", "10Gbps"
    speed: Optional[str] = Field(None, description="Port speed (e.g., '100Mbps', '1Gbps', '10Gbps')")
    
    # duplex: Whether the port can send and receive data at the same time
    # "full" means it can do both simultaneously, "half" means it can only do one at a time
    duplex: Optional[str] = Field(None, description="Duplex mode (e.g., 'full', 'half', 'auto')")


# VLAN CLASS - Represents Virtual Local Area Networks
# =============================================================================

class VLAN(BaseEntity):
    """
    VLAN (Virtual Local Area Network) model
    
    WHAT IS A VLAN?
    A VLAN is a way to virtually separate network traffic
    Think of it like having different "lanes" on a highway
    Even though all the cars (data) use the same physical road (network cables),
    they're separated into different lanes for different purposes
    
    For example:
    - VLAN 10 might be for office computers
    - VLAN 20 might be for printers
    - VLAN 30 might be for servers
    
    This separation improves security and performance
    """
    
    # TYPE FIELD - Ensures this entity is always marked as a VLAN
    type: Literal[EntityType.VLAN] = EntityType.VLAN
    
    # VLAN-SPECIFIC FIELDS - Information specific to VLANs
    # -------------------------------------------------------------------------
    
    # vlan_id: The unique number that identifies this VLAN
    # This is required because every VLAN must have an ID
    # Common practice: use numbers like 10, 20, 30, 100, etc.
    vlan_id: int = Field(..., description="VLAN ID number (e.g., 10, 20, 100)")
    
    # subnet: The IP address range for devices in this VLAN
    # Example: "192.168.10.0/24" means devices get IPs like 192.168.10.1, 192.168.10.2, etc.
    subnet: Optional[str] = Field(None, description="IP subnet for this VLAN (e.g., '192.168.10.0/24')")
    
    # gateway: The IP address that devices use to reach other networks
    # This is like the "exit door" from this VLAN to the internet or other networks
    gateway: Optional[str] = Field(None, description="Gateway IP address for this VLAN (e.g., '192.168.10.1')")
    
    # description: Human-readable description of what this VLAN is for
    description: Optional[str] = Field(None, description="Description of VLAN purpose (e.g., 'Office Computers', 'Printers')")


# SERVER CLASS - Represents physical servers
# =============================================================================

class Server(BaseEntity):
    """
    Physical Server model
    
    WHAT IS A SERVER?
    A server is a powerful computer that provides services to other computers
    Think of it like a "super computer" that can run multiple virtual computers
    or host websites, databases, and applications
    
    Servers are usually:
    - More powerful than regular computers
    - Designed to run 24/7 without stopping
    - Located in data centers or server rooms
    - Managed remotely by IT administrators
    """
    
    # TYPE FIELD - Ensures this entity is always marked as a server
    type: Literal[EntityType.SERVER] = EntityType.SERVER
    
    # SERVER-SPECIFIC FIELDS - Information specific to physical servers
    # -------------------------------------------------------------------------
    
    # hostname: The network name of this server
    # This is required because every server needs a name to identify it on the network
    # Example: "web-server-01", "database-server-primary"
    hostname: str = Field(..., description="Server hostname/network name (e.g., 'web-server-01')")
    
    # ip_address: The primary IP address of this server
    # This is how other computers connect to this server
    ip_address: Optional[str] = Field(None, description="Primary IP address (e.g., '192.168.1.100')")
    
    # mac_address: The unique hardware address of the server's network card
    mac_address: Optional[str] = Field(None, description="MAC address of primary network interface")
    
    # HARDWARE SPECIFICATIONS - Information about the server's physical capabilities
    # -------------------------------------------------------------------------
    
    # cpu_cores: How many CPU cores this server has
    # More cores = can handle more tasks simultaneously
    cpu_cores: Optional[int] = Field(None, description="Number of CPU cores (e.g., 8, 16, 32)")
    
    # memory_gb: How much RAM (memory) this server has
    # More memory = can run more applications and handle more data
    memory_gb: Optional[int] = Field(None, description="Amount of RAM in gigabytes (e.g., 32, 64, 128)")
    
    # storage_gb: How much disk storage this server has
    # More storage = can store more data, applications, and files
    storage_gb: Optional[int] = Field(None, description="Amount of disk storage in gigabytes (e.g., 1000, 2000)")
    
    # os: What operating system this server runs
    # Common examples: "Ubuntu 20.04", "Windows Server 2019", "CentOS 7"
    os: Optional[str] = Field(None, description="Operating system (e.g., 'Ubuntu 20.04', 'Windows Server 2019')")
    
    # rack_location: Where this server is physically located
    # Data centers use racks to organize servers, like bookshelves for books
    rack_location: Optional[str] = Field(None, description="Physical rack location (e.g., 'Rack 15, Unit 12')")


# VIRTUAL MACHINE CLASS - Represents virtual computers running on servers
# =============================================================================

class VirtualMachine(BaseEntity):
    """
    Virtual Machine model
    
    WHAT IS A VIRTUAL MACHINE?
    A virtual machine (VM) is like a "computer within a computer"
    It's software that pretends to be a real computer
    One physical server can run multiple virtual machines
    
    Think of it like having multiple apartments in one building:
    - The building is the physical server
    - Each apartment is a virtual machine
    - Each apartment has its own address (IP), utilities (CPU, memory), etc.
    - But they all share the same physical building infrastructure
    
    Benefits of VMs:
    - Better resource utilization (one server can host many VMs)
    - Easier backup and recovery
    - Can move VMs between servers
    - Isolation (if one VM crashes, others are unaffected)
    """
    
    # TYPE FIELD - Ensures this entity is always marked as a virtual machine
    type: Literal[EntityType.VIRTUAL_MACHINE] = EntityType.VIRTUAL_MACHINE
    
    # VM-SPECIFIC FIELDS - Information specific to virtual machines
    # -------------------------------------------------------------------------
    
    # hostname: The network name of this virtual machine
    # This is required because every VM needs a name to identify it
    hostname: str = Field(..., description="VM hostname/network name (e.g., 'web-vm-01')")
    
    # ip_address: The IP address assigned to this VM
    ip_address: Optional[str] = Field(None, description="VM IP address (e.g., '192.168.1.101')")
    
    # VIRTUAL HARDWARE SPECIFICATIONS - Resources allocated to this VM
    # -------------------------------------------------------------------------
    # These are "virtual" resources carved out from the physical server
    
    # cpu_cores: How many CPU cores are allocated to this VM
    # This is usually less than the total cores on the physical server
    cpu_cores: Optional[int] = Field(None, description="Number of allocated CPU cores (e.g., 2, 4, 8)")
    
    # memory_gb: How much RAM is allocated to this VM
    memory_gb: Optional[int] = Field(None, description="Amount of allocated RAM in gigabytes (e.g., 4, 8, 16)")
    
    # storage_gb: How much disk space is allocated to this VM
    storage_gb: Optional[int] = Field(None, description="Amount of allocated storage in gigabytes (e.g., 50, 100, 200)")
    
    # os: What operating system this VM runs
    # This can be different from the host server's OS
    os: Optional[str] = Field(None, description="Guest operating system (e.g., 'Ubuntu 20.04', 'Windows 10')")
    
    # VIRTUALIZATION INFORMATION - Details about the VM's virtualization
    # -------------------------------------------------------------------------
    
    # hypervisor: The software that manages this VM
    # Common examples: "VMware ESXi", "Microsoft Hyper-V", "KVM"
    hypervisor: Optional[str] = Field(None, description="Hypervisor type (e.g., 'VMware ESXi', 'Hyper-V', 'KVM')")
    
    # vm_id: The unique identifier used by the hypervisor
    # This is like a "license plate" for the VM within the virtualization system
    vm_id: Optional[str] = Field(None, description="VM identifier in hypervisor system")


# KUBERNETES POD CLASS - Represents Kubernetes pods
# =============================================================================

class KubernetesPod(BaseEntity):
    """
    Kubernetes Pod model
    
    WHAT IS KUBERNETES?
    Kubernetes is a system for managing containerized applications
    Think of it like a "container orchestrator" - it manages many containers
    running across many servers automatically
    
    WHAT IS A POD?
    A pod is the smallest unit in Kubernetes
    It's like a "wrapper" that contains one or more containers
    Think of it like a "pod" of dolphins swimming together
    
    Pods provide:
    - Shared network (all containers in a pod share the same IP)
    - Shared storage (containers can share files)
    - Lifecycle management (containers in a pod start and stop together)
    
    Most pods contain just one container, but they can contain multiple
    containers that need to work very closely together
    """
    
    # TYPE FIELD - Ensures this entity is always marked as a Kubernetes pod
    type: Literal[EntityType.KUBERNETES_POD] = EntityType.KUBERNETES_POD
    
    # POD-SPECIFIC FIELDS - Information specific to Kubernetes pods
    # -------------------------------------------------------------------------
    
    # namespace: The Kubernetes namespace this pod belongs to
    # This is required because every pod must belong to a namespace
    # Namespaces are like "folders" that organize resources
    # Common examples: "default", "kube-system", "production", "development"
    namespace: str = Field(..., description="Kubernetes namespace (e.g., 'default', 'production')")
    
    # pod_ip: The IP address assigned to this pod
    # All containers in the pod share this IP address
    pod_ip: Optional[str] = Field(None, description="Pod IP address (e.g., '10.244.0.15')")
    
    # node_name: Which Kubernetes node (server) this pod is running on
    # Kubernetes automatically chooses where to run pods
    node_name: Optional[str] = Field(None, description="Kubernetes node name where pod is running")
    
    # KUBERNETES METADATA - Information stored as JSON strings
    # -------------------------------------------------------------------------
    # Neo4j can't store complex dictionaries, so we store these as JSON strings
    
    # k8s_labels_json: Kubernetes labels stored as JSON
    # Labels are key-value pairs used to organize and select resources
    # Example: {"app": "web-server", "version": "1.0", "tier": "frontend"}
    k8s_labels_json: str = Field(default="{}", description="Kubernetes labels stored as JSON string")
    
    # annotations_json: Kubernetes annotations stored as JSON
    # Annotations are like labels but for storing non-identifying metadata
    # Example: {"deployment.kubernetes.io/revision": "1", "author": "john@company.com"}
    annotations_json: str = Field(default="{}", description="Kubernetes annotations stored as JSON string")
    
    # POD STATUS INFORMATION - Current state of the pod
    # -------------------------------------------------------------------------
    
    # phase: Current phase of the pod lifecycle
    # Common values: "Pending", "Running", "Succeeded", "Failed", "Unknown"
    phase: Optional[str] = Field(None, description="Pod phase (e.g., 'Running', 'Pending', 'Failed')")
    
    # restart_count: How many times containers in this pod have been restarted
    # High restart counts might indicate problems with the application
    restart_count: Optional[int] = Field(None, description="Number of times containers have been restarted")
    
    # VALIDATORS - Functions that convert dictionaries to JSON strings
    # -------------------------------------------------------------------------
    
    @validator('k8s_labels_json', pre=True)
    def serialize_k8s_labels(cls, v):
        """
        Convert Kubernetes labels dictionary to JSON string
        
        This validator works the same way as the properties validator
        If someone provides a dictionary for labels, it converts it to JSON
        """
        if isinstance(v, dict):
            return json.dumps(v)
        return v
    
    @validator('annotations_json', pre=True)
    def serialize_annotations(cls, v):
        """
        Convert Kubernetes annotations dictionary to JSON string
        
        Same as labels validator, but for annotations
        """
        if isinstance(v, dict):
            return json.dumps(v)
        return v
    
    # HELPER METHODS - Functions for working with Kubernetes metadata
    # -------------------------------------------------------------------------
    
    def set_k8s_labels(self, labels: Dict[str, str]) -> None:
        """
        Set Kubernetes labels for this pod
        
        EXAMPLE USAGE:
        pod = KubernetesPod(id="pod-001", name="web-pod", namespace="default")
        pod.set_k8s_labels({"app": "web-server", "version": "1.0"})
        """
        self.k8s_labels_json = json.dumps(labels)
    
    def get_k8s_labels(self) -> Dict[str, str]:
        """
        Get Kubernetes labels for this pod
        
        EXAMPLE USAGE:
        labels = pod.get_k8s_labels()  # Returns {"app": "web-server", "version": "1.0"}
        """
        try:
            return json.loads(self.k8s_labels_json)
        except json.JSONDecodeError:
            return {}
    
    def set_annotations(self, annotations: Dict[str, str]) -> None:
        """
        Set Kubernetes annotations for this pod
        
        EXAMPLE USAGE:
        pod.set_annotations({"deployment.kubernetes.io/revision": "1"})
        """
        self.annotations_json = json.dumps(annotations)
    
    def get_annotations(self) -> Dict[str, str]:
        """
        Get Kubernetes annotations for this pod
        
        EXAMPLE USAGE:
        annotations = pod.get_annotations()  # Returns the annotations dictionary
        """
        try:
            return json.loads(self.annotations_json)
        except json.JSONDecodeError:
            return {}


# CONTAINER CLASS - Represents individual application containers
# =============================================================================

class Container(BaseEntity):
    """
    Container model
    
    WHAT IS A CONTAINER?
    A container is like a "shipping container" for applications
    Just like shipping containers can hold different goods but all have the same
    standard size and can be moved by the same trucks and cranes,
    software containers can hold different applications but all run on the same
    container runtime and can be managed by the same tools
    
    Containers provide:
    - Isolation: Each container runs separately from others
    - Portability: Containers run the same way on any system
    - Efficiency: Containers share the host OS kernel (lighter than VMs)
    - Consistency: The same container works in development, testing, and production
    
    CONTAINER vs VIRTUAL MACHINE:
    - VMs virtualize entire computers (including the OS)
    - Containers virtualize just the application layer
    - Containers are lighter, faster, and more efficient
    - VMs provide stronger isolation
    """
    
    # TYPE FIELD - Ensures this entity is always marked as a container
    type: Literal[EntityType.CONTAINER] = EntityType.CONTAINER
    
    # CONTAINER-SPECIFIC FIELDS - Information specific to containers
    # -------------------------------------------------------------------------
    
    # image: The container image used to create this container
    # This is required because every container must be based on an image
    # Think of an image like a "template" or "recipe" for creating containers
    # Examples: "nginx:latest", "postgres:13", "python:3.9"
    image: str = Field(..., description="Container image name (e.g., 'nginx:latest', 'python:3.9')")
    
    # image_tag: The specific version/tag of the image
    # Common tags: "latest", "1.0", "stable", "alpine"
    image_tag: Optional[str] = Field(None, description="Image tag/version (e.g., 'latest', '1.0', 'alpine')")
    
    # container_id: The unique identifier assigned by the container runtime
    # This is like a "license plate" for the container
    container_id: Optional[str] = Field(None, description="Container runtime ID (unique identifier)")
    
    # NETWORK CONFIGURATION - How the container connects to the network
    # -------------------------------------------------------------------------
    
    # ports: List of network ports this container exposes
    # Stored as a list of strings because Neo4j can handle string arrays
    # Examples: ["80", "443", "8080:80"] (8080:80 means host port 8080 maps to container port 80)
    ports: List[str] = Field(default_factory=list, description="Exposed network ports (e.g., ['80', '443', '8080:80'])")
    
    # ENVIRONMENT CONFIGURATION - Environment variables for the container
    # -------------------------------------------------------------------------
    
    # environment_vars_json: Environment variables stored as JSON string
    # Environment variables are like "settings" that the application inside the container can read
    # Examples: {"DATABASE_URL": "postgresql://...", "API_KEY": "secret123"}
    environment_vars_json: str = Field(default="{}", description="Environment variables stored as JSON string")
    
    # RESOURCE LIMITS - How much resources this container can use
    # -------------------------------------------------------------------------
    
    # cpu_limit: Maximum CPU this container can use
    # Examples: "0.5" (half a CPU core), "1.0" (one CPU core), "2.0" (two CPU cores)
    cpu_limit: Optional[str] = Field(None, description="CPU limit (e.g., '0.5', '1.0', '2.0')")
    
    # memory_limit: Maximum memory this container can use
    # Examples: "512Mi" (512 megabytes), "1Gi" (1 gigabyte), "2Gi" (2 gigabytes)
    memory_limit: Optional[str] = Field(None, description="Memory limit (e.g., '512Mi', '1Gi', '2Gi')")
    
    # CONTAINER STATUS - Current state of the container
    # -------------------------------------------------------------------------
    
    # status: Current status of the container
    # Common values: "running", "stopped", "created", "restarting", "removing"
    status: Optional[str] = Field(None, description="Container status (e.g., 'running', 'stopped', 'restarting')")
    
    # VALIDATOR - Function that converts environment variables to JSON string
    # -------------------------------------------------------------------------
    
    @validator('environment_vars_json', pre=True)
    def serialize_environment_vars(cls, v):
        """
        Convert environment variables dictionary to JSON string
        
        This validator works the same way as the other validators
        If someone provides a dictionary for environment variables, it converts it to JSON
        """
        if isinstance(v, dict):
            return json.dumps(v)
        return v
    
    # HELPER METHODS - Functions for working with environment variables
    # -------------------------------------------------------------------------
    
    def set_environment_vars(self, env_vars: Dict[str, str]) -> None:
        """
        Set environment variables for this container
        
        EXAMPLE USAGE:
        container = Container(id="cont-001", name="web-container", image="nginx:latest")
        container.set_environment_vars({"PORT": "8080", "DEBUG": "true"})
        """
        self.environment_vars_json = json.dumps(env_vars)
    
    def get_environment_vars(self) -> Dict[str, str]:
        """
        Get environment variables for this container
        
        EXAMPLE USAGE:
        env_vars = container.get_environment_vars()  # Returns {"PORT": "8080", "DEBUG": "true"}
        """
        try:
            return json.loads(self.environment_vars_json)
        except json.JSONDecodeError:
            return {}


# RELATIONSHIP CLASS - Represents connections between entities
# =============================================================================

class Relationship(BaseModel):
    """
    Model for relationships between entities
    
    WHAT IS A RELATIONSHIP?
    In a graph database, relationships connect entities together
    Think of entities as "dots" and relationships as "lines" connecting the dots
    
    For example:
    - A server HOSTS a virtual machine
    - A virtual machine RUNS a Kubernetes pod
    - A pod CONTAINS a container
    - A container CONNECTS_TO a network port
    
    Relationships have:
    - A source (where the relationship starts)
    - A target (where the relationship ends)
    - A type (what kind of relationship it is)
    - Properties (additional information about the relationship)
    """
    
    # RELATIONSHIP CORE FIELDS - Basic information about the relationship
    # -------------------------------------------------------------------------
    
    # source_id: The ID of the entity where this relationship starts
    # This is required because every relationship must have a source
    source_id: str = Field(..., description="ID of the source entity (where relationship starts)")
    
    # target_id: The ID of the entity where this relationship ends
    # This is required because every relationship must have a target
    target_id: str = Field(..., description="ID of the target entity (where relationship ends)")
    
    # relationship_type: What kind of relationship this is
    # This is required because we need to know the type of connection
    # Examples: "HOSTS", "RUNS", "CONTAINS", "CONNECTS_TO"
    relationship_type: str = Field(..., description="Type of relationship (e.g., 'HOSTS', 'RUNS', 'CONTAINS')")
    
    # properties_json: Additional properties about this relationship
    # Stored as JSON string for Neo4j compatibility
    # Examples: {"bandwidth": "1Gbps", "connection_type": "primary"}
    properties_json: str = Field(default="{}", description="Additional relationship properties stored as JSON string")
    
    # created_at: When this relationship was created
    created_at: datetime = Field(default_factory=datetime.now, description="When this relationship was created")
    
    # VALIDATOR - Function that converts properties to JSON string
    # -------------------------------------------------------------------------
    
    @validator('properties_json', pre=True)
    def serialize_properties(cls, v):
        """
        Convert relationship properties dictionary to JSON string
        
        Same as the other validators - converts dictionaries to JSON strings
        """
        if isinstance(v, dict):
            return json.dumps(v)
        return v
    
    # HELPER METHODS - Functions for working with relationship properties
    # -------------------------------------------------------------------------
    
    def set_properties(self, properties: Dict[str, Any]) -> None:
        """
        Set additional properties for this relationship
        
        EXAMPLE USAGE:
        rel = Relationship(source_id="server-001", target_id="vm-001", relationship_type="HOSTS")
        rel.set_properties({"allocation_date": "2023-01-15", "resource_pool": "production"})
        """
        self.properties_json = json.dumps(properties)
    
    def get_properties(self) -> Dict[str, Any]:
        """
        Get additional properties for this relationship
        
        EXAMPLE USAGE:
        props = rel.get_properties()  # Returns the properties dictionary
        """
        try:
            return json.loads(self.properties_json)
        except json.JSONDecodeError:
            return {}


# RELATIONSHIP TYPE ENUMERATION - Predefined list of relationship types
# =============================================================================

class RelationshipType(str, Enum):
    """
    Enumeration of all possible relationship types in our network infrastructure
    
    This enum defines all the ways that entities can be connected to each other
    Using an enum prevents typos and ensures consistency
    
    RELATIONSHIP TYPES EXPLAINED:
    """
    
    # NETWORK LAYER RELATIONSHIPS
    # -------------------------------------------------------------------------
    
    # CONNECTED_TO: Physical or logical network connections
    # Examples: Container CONNECTED_TO NetworkPort, Server CONNECTED_TO NetworkPort
    CONNECTED_TO = "CONNECTED_TO"
    
    # BELONGS_TO: Membership relationships
    # Examples: NetworkPort BELONGS_TO VLAN, VirtualMachine BELONGS_TO Server
    BELONGS_TO = "BELONGS_TO"
    
    # PART_OF: Component relationships
    # Examples: NetworkPort PART_OF NetworkSwitch
    PART_OF = "PART_OF"
    
    # COMPUTE LAYER RELATIONSHIPS
    # -------------------------------------------------------------------------
    
    # HOSTS: When one entity provides resources for another
    # Examples: Server HOSTS VirtualMachine, VirtualMachine HOSTS KubernetesPod
    HOSTS = "HOSTS"
    
    # RUNS_ON: When one entity runs on top of another
    # Examples: VirtualMachine RUNS_ON Server, KubernetesPod RUNS_ON VirtualMachine
    RUNS_ON = "RUNS_ON"
    
    # APPLICATION LAYER RELATIONSHIPS
    # -------------------------------------------------------------------------
    
    # CONTAINS: When one entity contains another
    # Examples: KubernetesPod CONTAINS Container, VLAN CONTAINS Server
    CONTAINS = "CONTAINS"
    
    # DEPLOYED_ON: When an application is deployed on infrastructure
    # Examples: Container DEPLOYED_ON KubernetesPod
    DEPLOYED_ON = "DEPLOYED_ON" 