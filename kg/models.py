"""
Pydantic models for network infrastructure entities
"""
from typing import Optional, List, Dict, Any, Literal, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum
import json


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
    # Store as JSON string for Neo4j compatibility
    properties_json: str = Field(default="{}", description="Additional properties as JSON")
    neo4j_labels: List[str] = Field(default_factory=list, description="Neo4j labels")
    
    @validator('properties_json', pre=True)
    def serialize_properties(cls, v):
        if isinstance(v, dict):
            return json.dumps(v)
        return v
    
    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Set additional properties"""
        self.properties_json = json.dumps(properties)
    
    def get_properties(self) -> Dict[str, Any]:
        """Get additional properties"""
        try:
            return json.loads(self.properties_json)
        except json.JSONDecodeError:
            return {}


class NetworkSwitch(BaseEntity):
    """Network Switch model"""
    type: Literal[EntityType.NETWORK_SWITCH] = EntityType.NETWORK_SWITCH
    model: Optional[str] = Field(None, description="Switch model")
    vendor: Optional[str] = Field(None, description="Switch vendor")
    ip_address: Optional[str] = Field(None, description="Management IP address")
    mac_address: Optional[str] = Field(None, description="MAC address")
    port_count: Optional[int] = Field(None, description="Number of ports")
    location: Optional[str] = Field(None, description="Physical location")


class NetworkPort(BaseEntity):
    """Network Port model"""
    type: Literal[EntityType.NETWORK_PORT] = EntityType.NETWORK_PORT
    port_number: int = Field(..., description="Port number on the switch")
    port_type: Optional[str] = Field(None, description="Port type (e.g., FastEthernet, GigabitEthernet)")
    status: Optional[str] = Field(None, description="Port status (up/down)")
    speed: Optional[str] = Field(None, description="Port speed")
    duplex: Optional[str] = Field(None, description="Duplex mode")


class VLAN(BaseEntity):
    """VLAN model"""
    type: Literal[EntityType.VLAN] = EntityType.VLAN
    vlan_id: int = Field(..., description="VLAN ID")
    subnet: Optional[str] = Field(None, description="Subnet associated with VLAN")
    gateway: Optional[str] = Field(None, description="Gateway IP")
    description: Optional[str] = Field(None, description="VLAN description")


class Server(BaseEntity):
    """Physical Server model"""
    type: Literal[EntityType.SERVER] = EntityType.SERVER
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
    type: Literal[EntityType.VIRTUAL_MACHINE] = EntityType.VIRTUAL_MACHINE
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
    type: Literal[EntityType.KUBERNETES_POD] = EntityType.KUBERNETES_POD
    namespace: str = Field(..., description="Kubernetes namespace")
    pod_ip: Optional[str] = Field(None, description="Pod IP address")
    node_name: Optional[str] = Field(None, description="Kubernetes node name")
    # Store as JSON strings for Neo4j compatibility
    k8s_labels_json: str = Field(default="{}", description="Kubernetes labels as JSON")
    annotations_json: str = Field(default="{}", description="Kubernetes annotations as JSON")
    phase: Optional[str] = Field(None, description="Pod phase (Running, Pending, etc.)")
    restart_count: Optional[int] = Field(None, description="Container restart count")
    
    @validator('k8s_labels_json', pre=True)
    def serialize_k8s_labels(cls, v):
        if isinstance(v, dict):
            return json.dumps(v)
        return v
    
    @validator('annotations_json', pre=True)
    def serialize_annotations(cls, v):
        if isinstance(v, dict):
            return json.dumps(v)
        return v
    
    def set_k8s_labels(self, labels: Dict[str, str]) -> None:
        """Set Kubernetes labels"""
        self.k8s_labels_json = json.dumps(labels)
    
    def get_k8s_labels(self) -> Dict[str, str]:
        """Get Kubernetes labels"""
        try:
            return json.loads(self.k8s_labels_json)
        except json.JSONDecodeError:
            return {}
    
    def set_annotations(self, annotations: Dict[str, str]) -> None:
        """Set Kubernetes annotations"""
        self.annotations_json = json.dumps(annotations)
    
    def get_annotations(self) -> Dict[str, str]:
        """Get Kubernetes annotations"""
        try:
            return json.loads(self.annotations_json)
        except json.JSONDecodeError:
            return {}


class Container(BaseEntity):
    """Container model"""
    type: Literal[EntityType.CONTAINER] = EntityType.CONTAINER
    image: str = Field(..., description="Container image")
    image_tag: Optional[str] = Field(None, description="Image tag")
    container_id: Optional[str] = Field(None, description="Container runtime ID")
    # Store as simple array for Neo4j compatibility
    ports: List[str] = Field(default_factory=list, description="Exposed ports")
    # Store as JSON string for Neo4j compatibility
    environment_vars_json: str = Field(default="{}", description="Environment variables as JSON")
    cpu_limit: Optional[str] = Field(None, description="CPU limit")
    memory_limit: Optional[str] = Field(None, description="Memory limit")
    status: Optional[str] = Field(None, description="Container status")
    
    @validator('environment_vars_json', pre=True)
    def serialize_environment_vars(cls, v):
        if isinstance(v, dict):
            return json.dumps(v)
        return v
    
    def set_environment_vars(self, env_vars: Dict[str, str]) -> None:
        """Set environment variables"""
        self.environment_vars_json = json.dumps(env_vars)
    
    def get_environment_vars(self) -> Dict[str, str]:
        """Get environment variables"""
        try:
            return json.loads(self.environment_vars_json)
        except json.JSONDecodeError:
            return {}


class Relationship(BaseModel):
    """Model for relationships between entities"""
    source_id: str = Field(..., description="Source entity ID")
    target_id: str = Field(..., description="Target entity ID")
    relationship_type: str = Field(..., description="Type of relationship")
    # Store as JSON string for Neo4j compatibility
    properties_json: str = Field(default="{}", description="Relationship properties as JSON")
    created_at: datetime = Field(default_factory=datetime.now)
    
    @validator('properties_json', pre=True)
    def serialize_properties(cls, v):
        if isinstance(v, dict):
            return json.dumps(v)
        return v
    
    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Set relationship properties"""
        self.properties_json = json.dumps(properties)
    
    def get_properties(self) -> Dict[str, Any]:
        """Get relationship properties"""
        try:
            return json.loads(self.properties_json)
        except json.JSONDecodeError:
            return {}


# Relationship types
class RelationshipType(str, Enum):
    CONNECTED_TO = "CONNECTED_TO"
    HOSTS = "HOSTS"
    RUNS_ON = "RUNS_ON"
    BELONGS_TO = "BELONGS_TO"
    CONTAINS = "CONTAINS"
    DEPLOYED_ON = "DEPLOYED_ON"
    PART_OF = "PART_OF" 