"""
Pydantic models for network infrastructure entities
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class EntityType(str, Enum):
    NETWORK_SWITCH = "NetworkSwitch"
    NETWORK_PORT = "NetworkPort"
    VLAN = "VLAN"
    SERVER = "Server"
    VIRTUAL_MACHINE = "VirtualMachine"
    KUBERNETES_POD = "KubernetesPod"
    CONTAINER = "Container"


class BaseEntity(BaseModel):
    """Base model for all network infrastructure entities"""
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Human-readable name")
    type: EntityType = Field(..., description="Entity type")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    properties: Dict[str, Any] = Field(default_factory=dict, description="Additional properties")
    labels: List[str] = Field(default_factory=list, description="Neo4j labels")


class NetworkSwitch(BaseEntity):
    """Network Switch model"""
    type: EntityType = Field(default=EntityType.NETWORK_SWITCH, const=True)
    model: Optional[str] = Field(None, description="Switch model")
    vendor: Optional[str] = Field(None, description="Switch vendor")
    ip_address: Optional[str] = Field(None, description="Management IP address")
    mac_address: Optional[str] = Field(None, description="MAC address")
    port_count: Optional[int] = Field(None, description="Number of ports")
    location: Optional[str] = Field(None, description="Physical location")


class NetworkPort(BaseEntity):
    """Network Port model"""
    type: EntityType = Field(default=EntityType.NETWORK_PORT, const=True)
    port_number: int = Field(..., description="Port number on the switch")
    port_type: Optional[str] = Field(None, description="Port type (e.g., FastEthernet, GigabitEthernet)")
    status: Optional[str] = Field(None, description="Port status (up/down)")
    speed: Optional[str] = Field(None, description="Port speed")
    duplex: Optional[str] = Field(None, description="Duplex mode")


class VLAN(BaseEntity):
    """VLAN model"""
    type: EntityType = Field(default=EntityType.VLAN, const=True)
    vlan_id: int = Field(..., description="VLAN ID")
    subnet: Optional[str] = Field(None, description="Subnet associated with VLAN")
    gateway: Optional[str] = Field(None, description="Gateway IP")
    description: Optional[str] = Field(None, description="VLAN description")


class Server(BaseEntity):
    """Physical Server model"""
    type: EntityType = Field(default=EntityType.SERVER, const=True)
    hostname: str = Field(..., description="Server hostname")
    ip_address: Optional[str] = Field(None, description="Primary IP address")
    mac_address: Optional[str] = Field(None, description="MAC address")
    cpu_cores: Optional[int] = Field(None, description="Number of CPU cores")
    memory_gb: Optional[int] = Field(None, description="Memory in GB")
    storage_gb: Optional[int] = Field(None, description="Storage in GB")
    os: Optional[str] = Field(None, description="Operating system")
    rack_location: Optional[str] = Field(None, description="Rack location")


class VirtualMachine(BaseEntity):
    """Virtual Machine model"""
    type: EntityType = Field(default=EntityType.VIRTUAL_MACHINE, const=True)
    hostname: str = Field(..., description="VM hostname")
    ip_address: Optional[str] = Field(None, description="VM IP address")
    cpu_cores: Optional[int] = Field(None, description="Allocated CPU cores")
    memory_gb: Optional[int] = Field(None, description="Allocated memory in GB")
    storage_gb: Optional[int] = Field(None, description="Allocated storage in GB")
    os: Optional[str] = Field(None, description="Guest operating system")
    hypervisor: Optional[str] = Field(None, description="Hypervisor type")
    vm_id: Optional[str] = Field(None, description="VM ID in hypervisor")


class KubernetesPod(BaseEntity):
    """Kubernetes Pod model"""
    type: EntityType = Field(default=EntityType.KUBERNETES_POD, const=True)
    namespace: str = Field(..., description="Kubernetes namespace")
    pod_ip: Optional[str] = Field(None, description="Pod IP address")
    node_name: Optional[str] = Field(None, description="Kubernetes node name")
    labels: Dict[str, str] = Field(default_factory=dict, description="Kubernetes labels")
    annotations: Dict[str, str] = Field(default_factory=dict, description="Kubernetes annotations")
    phase: Optional[str] = Field(None, description="Pod phase (Running, Pending, etc.)")
    restart_count: Optional[int] = Field(None, description="Container restart count")


class Container(BaseEntity):
    """Container model"""
    type: EntityType = Field(default=EntityType.CONTAINER, const=True)
    image: str = Field(..., description="Container image")
    image_tag: Optional[str] = Field(None, description="Image tag")
    container_id: Optional[str] = Field(None, description="Container runtime ID")
    ports: List[str] = Field(default_factory=list, description="Exposed ports")
    environment_vars: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    cpu_limit: Optional[str] = Field(None, description="CPU limit")
    memory_limit: Optional[str] = Field(None, description="Memory limit")
    status: Optional[str] = Field(None, description="Container status")


class Relationship(BaseModel):
    """Model for relationships between entities"""
    source_id: str = Field(..., description="Source entity ID")
    target_id: str = Field(..., description="Target entity ID")
    relationship_type: str = Field(..., description="Type of relationship")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Relationship properties")
    created_at: datetime = Field(default_factory=datetime.now)


# Relationship types
class RelationshipType(str, Enum):
    CONNECTED_TO = "CONNECTED_TO"
    HOSTS = "HOSTS"
    RUNS_ON = "RUNS_ON"
    BELONGS_TO = "BELONGS_TO"
    CONTAINS = "CONTAINS"
    DEPLOYED_ON = "DEPLOYED_ON"
    PART_OF = "PART_OF" 