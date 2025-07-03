# =============================================================================
# CONFIG.PY - CONFIGURATION SETTINGS FOR THE NETWORK INFRASTRUCTURE KNOWLEDGE GRAPH
# =============================================================================
# This file contains all the settings and configuration for our knowledge graph system
# Think of it like a "control panel" where we can adjust how our software behaves
# Instead of hardcoding values in our code, we put them here so they're easy to change

# DOCSTRING - Documentation that explains what this file does
# =============================================================================
"""
Configuration settings for the Network Infrastructure Knowledge Graph

This file manages all the settings our software needs to run properly.
It handles things like:
- Database connection details (where to find Neo4j)
- How much sample data to generate
- Which environment we're running in (development, production, testing)
- Security settings and passwords

The configuration is organized into classes, which are like "blueprints" 
that group related settings together.
"""

# IMPORT STATEMENTS - Getting tools we need from other Python libraries
# =============================================================================

# os: This is a built-in Python library that helps us interact with the operating system
# We use it to read environment variables (settings stored in the computer's environment)
import os

# typing: This helps us specify what type of data our functions expect
# It's like putting "labels" on our code to make it clearer and catch errors
from typing import Dict, Any


# MAIN CONFIGURATION CLASS - The central place for all our settings
# =============================================================================

class Config:
    """
    Configuration class for the knowledge graph system
    
    WHAT IS A CLASS?
    A class is like a "blueprint" or "template" for organizing related data and functions.
    Think of it like a filing cabinet with different drawers for different types of information.
    
    This Config class is our "settings filing cabinet" where we organize all the
    configuration values our software needs to run.
    """
    
    # NEO4J DATABASE CONFIGURATION SECTION
    # -------------------------------------------------------------------------
    # These settings tell our software how to connect to the Neo4j database
    # Neo4j is where we store all our network topology data (switches, servers, etc.)
    
    # NEO4J_URI: This is the "address" of our Neo4j database
    # Think of it like a street address - it tells our software where to find the database
    # os.getenv() looks for an environment variable named "NEO4J_URI"
    # If it doesn't find one, it uses the default value "bolt://localhost:7687"
    # "bolt://" is the protocol (like "http://") that Neo4j uses for connections
    # "localhost:7687" means the database is running on the same computer, port 7687
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    
    # NEO4J_USERNAME: The username to log into the database
    # Like a username for any account, this identifies who is connecting
    # Default is "neo4j" which is Neo4j's standard admin username
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    
    # NEO4J_PASSWORD: The password to log into the database
    # This is kept secret for security - we never hardcode passwords in our code
    # Instead, we read it from an environment variable or use a default for development
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    
    # NEO4J_DATABASE: Which specific database to use within Neo4j
    # Neo4j can have multiple databases, like having multiple filing cabinets
    # "neo4j" is the default database name
    NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")
    
    # APPLICATION CONFIGURATION SECTION
    # -------------------------------------------------------------------------
    # These settings control how our application behaves overall
    
    # LOG_LEVEL: How much detail to show in log messages
    # "INFO" means show important information but not detailed debug messages
    # Other options: "DEBUG" (show everything), "WARNING" (show only problems), "ERROR" (show only serious problems)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # ENVIRONMENT: Which environment we're running in
    # "development" means we're still building/testing the software
    # Other options: "production" (live system), "testing" (automated tests)
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # DATA GENERATION SETTINGS SECTION
    # -------------------------------------------------------------------------
    # These settings control how much sample data our software creates
    # When we run the software, it can generate fake network data for testing
    
    # GENERATE_SAMPLE_DATA: Whether to create sample data or not
    # os.getenv() returns a string, so we compare it to "true" to get a boolean (True/False)
    # .lower() makes it case-insensitive, so "True", "TRUE", "true" all work
    GENERATE_SAMPLE_DATA = os.getenv("GENERATE_SAMPLE_DATA", "true").lower() == "true"
    
    # SWITCH_COUNT: How many network switches to create
    # int() converts the string from environment variable to a number
    # Default is 3 switches
    SWITCH_COUNT = int(os.getenv("SWITCH_COUNT", "3"))
    
    # PORTS_PER_SWITCH: How many network ports each switch has
    # Real network switches typically have 24 or 48 ports
    # Default is 24 ports per switch
    PORTS_PER_SWITCH = int(os.getenv("PORTS_PER_SWITCH", "24"))
    
    # VLAN_COUNT: How many VLANs (Virtual Local Area Networks) to create
    # VLANs are virtual network segments that separate different types of traffic
    # Default is 10 VLANs
    VLAN_COUNT = int(os.getenv("VLAN_COUNT", "10"))
    
    # SERVER_COUNT: How many physical servers to create
    # These are the physical computers that host virtual machines
    # Default is 5 servers
    SERVER_COUNT = int(os.getenv("SERVER_COUNT", "5"))
    
    # VMS_PER_SERVER: How many virtual machines each server runs
    # Virtual machines are like "computers within computers"
    # Default is 10 VMs per server
    VMS_PER_SERVER = int(os.getenv("VMS_PER_SERVER", "10"))
    
    # PODS_PER_VM: How many Kubernetes pods each virtual machine runs
    # Pods are containers that run applications in Kubernetes
    # Default is 100 pods per VM (this creates a realistic large-scale scenario)
    PODS_PER_VM = int(os.getenv("PODS_PER_VM", "100"))
    
    # CLASS METHODS - Functions that belong to the class
    # -------------------------------------------------------------------------
    # These are like "helper functions" that organize our configuration data
    
    @classmethod
    def get_neo4j_config(cls) -> Dict[str, str]:
        """
        Get Neo4j connection configuration
        
        WHAT IS A CLASS METHOD?
        @classmethod means this function belongs to the class itself, not to individual instances
        Think of it like a "class function" that can be called without creating an object
        
        WHAT IS A DICTIONARY?
        Dict[str, str] means this function returns a dictionary (like a phone book)
        where both keys and values are strings
        
        This function packages all the Neo4j settings into a neat dictionary
        that other parts of our code can easily use
        """
        return {
            "uri": cls.NEO4J_URI,        # Database address
            "username": cls.NEO4J_USERNAME,  # Login username
            "password": cls.NEO4J_PASSWORD,  # Login password
            "database": cls.NEO4J_DATABASE   # Which database to use
        }
    
    @classmethod
    def get_data_generation_config(cls) -> Dict[str, Any]:
        """
        Get data generation configuration
        
        Dict[str, Any] means a dictionary with string keys and values of any type
        (numbers, booleans, strings, etc.)
        
        This function packages all the data generation settings into a dictionary
        so other parts of our code can easily access them
        """
        return {
            "generate_sample_data": cls.GENERATE_SAMPLE_DATA,  # Whether to generate data
            "switch_count": cls.SWITCH_COUNT,                  # Number of switches
            "ports_per_switch": cls.PORTS_PER_SWITCH,         # Ports per switch
            "vlan_count": cls.VLAN_COUNT,                     # Number of VLANs
            "server_count": cls.SERVER_COUNT,                 # Number of servers
            "vms_per_server": cls.VMS_PER_SERVER,             # VMs per server
            "pods_per_vm": cls.PODS_PER_VM                    # Pods per VM
        }
    
    @classmethod
    def display_config(cls) -> None:
        """
        Display current configuration
        
        -> None means this function doesn't return anything
        It just prints information to the screen
        
        This function shows all the current settings in a readable format
        It's useful for debugging and confirming what settings are being used
        """
        print("Current Configuration:")
        print(f"  Neo4j URI: {cls.NEO4J_URI}")
        print(f"  Neo4j Username: {cls.NEO4J_USERNAME}")
        
        # For the password, we show asterisks (*) instead of the actual password
        # This is a security measure to prevent passwords from being displayed
        # len() gets the length of the password string
        # '*' * len() creates a string of asterisks the same length as the password
        print(f"  Neo4j Password: {'*' * len(cls.NEO4J_PASSWORD)}")
        
        print(f"  Environment: {cls.ENVIRONMENT}")
        print(f"  Log Level: {cls.LOG_LEVEL}")
        print(f"  Generate Sample Data: {cls.GENERATE_SAMPLE_DATA}")


# ENVIRONMENT-SPECIFIC CONFIGURATION CLASSES
# =============================================================================
# These classes inherit from the main Config class and override specific settings
# Think of them as "specialized versions" of the main configuration

class DevelopmentConfig(Config):
    """
    Development environment configuration
    
    WHAT IS INHERITANCE?
    When we write "class DevelopmentConfig(Config)", we're saying:
    "DevelopmentConfig is a special type of Config that inherits all the settings
    from Config but can override some of them"
    
    This is for when developers are working on the software
    We want more detailed logging and different settings than production
    """
    # Override the environment setting
    ENVIRONMENT = "development"
    
    # Override the log level to show more detailed information
    # "DEBUG" shows everything, including detailed technical information
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """
    Production environment configuration
    
    This is for when the software is running in a live environment
    serving real users. We want different settings than development:
    - Less detailed logging (for performance)
    - No sample data generation (we use real data)
    - More security-focused settings
    """
    ENVIRONMENT = "production"
    
    # "INFO" level logging shows important information but not debug details
    # This improves performance and reduces log file size
    LOG_LEVEL = "INFO"
    
    # In production, we don't want to generate fake sample data
    # We work with real network data instead
    GENERATE_SAMPLE_DATA = False


class TestingConfig(Config):
    """
    Testing environment configuration
    
    This is for when we run automated tests on our software
    We want smaller amounts of data and a separate database
    so tests run quickly and don't interfere with real data
    """
    ENVIRONMENT = "testing"
    
    # "DEBUG" level for testing so we can see what's happening
    LOG_LEVEL = "DEBUG"
    
    # Use a separate database for testing
    # This prevents tests from accidentally modifying real data
    NEO4J_DATABASE = "test"
    
    # Smaller amounts of sample data for faster testing
    SWITCH_COUNT = 1      # Only 1 switch instead of 3
    SERVER_COUNT = 2      # Only 2 servers instead of 5
    VMS_PER_SERVER = 2    # Only 2 VMs per server instead of 10
    PODS_PER_VM = 5       # Only 5 pods per VM instead of 100


# CONFIGURATION FACTORY FUNCTION
# =============================================================================
# This function helps us choose which configuration to use based on the environment

def get_config(environment: str = None) -> Config:
    """
    Get configuration based on environment
    
    WHAT IS A FUNCTION?
    A function is like a "mini-program" that takes inputs and produces outputs
    
    PARAMETERS:
    environment: str = None means:
    - The function expects a string parameter called 'environment'
    - If no environment is provided, it defaults to None
    
    RETURN TYPE:
    -> Config means this function returns a Config object
    
    This function acts like a "configuration factory" that produces the right
    configuration based on what environment we're running in
    """
    # If no environment was provided, try to get it from environment variables
    # or default to "development"
    environment = environment or os.getenv("ENVIRONMENT", "development")
    
    # Create a dictionary that maps environment names to configuration classes
    # This is like a "lookup table" or "menu" of available configurations
    config_map = {
        "development": DevelopmentConfig,   # For developers working on the code
        "production": ProductionConfig,     # For live systems serving users
        "testing": TestingConfig           # For automated testing
    }
    
    # Look up the environment in our map and get the corresponding configuration class
    # config_map.get() tries to find the environment in our dictionary
    # If it's not found, it defaults to DevelopmentConfig
    # The () at the end creates an instance of the configuration class
    return config_map.get(environment, DevelopmentConfig)() 