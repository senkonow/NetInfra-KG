"""
Configuration settings for the Network Infrastructure Knowledge Graph
"""
import os
from typing import Dict, Any


class Config:
    """Configuration class for the knowledge graph system"""
    
    # Neo4j Database Configuration
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")
    
    # Application Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # Data Generation Settings
    GENERATE_SAMPLE_DATA = os.getenv("GENERATE_SAMPLE_DATA", "true").lower() == "true"
    SWITCH_COUNT = int(os.getenv("SWITCH_COUNT", "3"))
    PORTS_PER_SWITCH = int(os.getenv("PORTS_PER_SWITCH", "24"))
    VLAN_COUNT = int(os.getenv("VLAN_COUNT", "10"))
    SERVER_COUNT = int(os.getenv("SERVER_COUNT", "5"))
    VMS_PER_SERVER = int(os.getenv("VMS_PER_SERVER", "10"))
    PODS_PER_VM = int(os.getenv("PODS_PER_VM", "100"))
    
    @classmethod
    def get_neo4j_config(cls) -> Dict[str, str]:
        """Get Neo4j connection configuration"""
        return {
            "uri": cls.NEO4J_URI,
            "username": cls.NEO4J_USERNAME,
            "password": cls.NEO4J_PASSWORD,
            "database": cls.NEO4J_DATABASE
        }
    
    @classmethod
    def get_data_generation_config(cls) -> Dict[str, Any]:
        """Get data generation configuration"""
        return {
            "generate_sample_data": cls.GENERATE_SAMPLE_DATA,
            "switch_count": cls.SWITCH_COUNT,
            "ports_per_switch": cls.PORTS_PER_SWITCH,
            "vlan_count": cls.VLAN_COUNT,
            "server_count": cls.SERVER_COUNT,
            "vms_per_server": cls.VMS_PER_SERVER,
            "pods_per_vm": cls.PODS_PER_VM
        }
    
    @classmethod
    def display_config(cls) -> None:
        """Display current configuration"""
        print("Current Configuration:")
        print(f"  Neo4j URI: {cls.NEO4J_URI}")
        print(f"  Neo4j Username: {cls.NEO4J_USERNAME}")
        print(f"  Neo4j Password: {'*' * len(cls.NEO4J_PASSWORD)}")
        print(f"  Environment: {cls.ENVIRONMENT}")
        print(f"  Log Level: {cls.LOG_LEVEL}")
        print(f"  Generate Sample Data: {cls.GENERATE_SAMPLE_DATA}")


# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development environment configuration"""
    ENVIRONMENT = "development"
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production environment configuration"""
    ENVIRONMENT = "production"
    LOG_LEVEL = "INFO"
    GENERATE_SAMPLE_DATA = False


class TestingConfig(Config):
    """Testing environment configuration"""
    ENVIRONMENT = "testing"
    LOG_LEVEL = "DEBUG"
    NEO4J_DATABASE = "test"
    SWITCH_COUNT = 1
    SERVER_COUNT = 2
    VMS_PER_SERVER = 2
    PODS_PER_VM = 5


# Configuration factory
def get_config(environment: str = None) -> Config:
    """Get configuration based on environment"""
    environment = environment or os.getenv("ENVIRONMENT", "development")
    
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    
    return config_map.get(environment, DevelopmentConfig)() 