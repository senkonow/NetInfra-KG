# =============================================================================
# SETUP.PY - PYTHON PACKAGE INSTALLATION CONFIGURATION FILE
# =============================================================================
# This file tells Python how to install our knowledge graph software as a package
# Think of it like an "instruction manual" for installing our software
# When someone runs "pip install ." or "uv add .", Python reads this file
# to understand what our software needs and how to install it properly

# IMPORT STATEMENTS - Getting tools we need from other Python libraries
# =============================================================================

# setuptools is a Python library that helps us package our software
# It's like a "packaging factory" that bundles our code for distribution
from setuptools import setup, find_packages

# THE MAIN SETUP FUNCTION - This is where we describe our software package
# =============================================================================
setup(
    # PACKAGE IDENTIFICATION - Basic information about our software
    # -------------------------------------------------------------------------
    
    # name: This is the official name of our software package
    # When someone installs it, they'll use this name
    # Think of it like the "brand name" of our software
    name="network-infrastructure-kg",
    
    # version: This tells people which version of our software they're using
    # We use "0.1.0" which means it's the first version (0.1) with no patches (0)
    # Version numbers help track updates and bug fixes
    version="0.1.0",
    
    # description: A short explanation of what our software does
    # This helps people understand the purpose of our software
    description="Neo4j Knowledge Graph for Network Infrastructure Topology",
    
    # author: Who created this software
    # This gives credit to the development team
    author="Infrastructure Team",
    
    # PACKAGE DISCOVERY - Finding all the code files to include
    # -------------------------------------------------------------------------
    
    # packages: This tells Python which folders contain our code
    # find_packages() is a smart function that automatically finds all folders
    # with Python code (any folder that has an __init__.py file)
    # In our case, it will find the 'kg' folder which contains our main code
    packages=find_packages(),
    
    # DEPENDENCIES - Other software our program needs to work
    # -------------------------------------------------------------------------
    
    # install_requires: This is a list of other Python packages our software needs
    # Think of these like "ingredients" - our software can't work without them
    # When someone installs our software, Python will automatically install these too
    install_requires=[
        # neo4j: This is the official Python library for connecting to Neo4j database
        # ">=5.17.0" means we need version 5.17.0 or newer
        # Neo4j is the graph database where we store our network topology data
        "neo4j>=5.17.0",
        
        # python-dotenv: This helps us read configuration from .env files
        # .env files are used to store passwords and settings safely
        # It's like a "settings file" that doesn't get shared publicly
        "python-dotenv>=1.0.0",
        
        # pydantic: This helps us validate and structure our data
        # It's like a "data checker" that makes sure our data is correct
        # For example, it ensures IP addresses look like real IP addresses
        "pydantic>=2.6.1",
        
        # fastapi: This helps us create web APIs (web services)
        # It's like a "web server toolkit" for our software
        # APIs let other programs talk to our knowledge graph
        "fastapi>=0.109.2",
        
        # uvicorn: This is a web server that runs our FastAPI application
        # Think of it as the "engine" that powers our web service
        # It handles incoming web requests and sends responses
        "uvicorn>=0.27.1",
        
        # requests: This helps our software make web requests to other services
        # It's like a "web browser" for our code
        # We use it to download data or communicate with other systems
        "requests>=2.31.0",
        
        # pandas: This is a powerful library for working with data tables
        # Think of it like "Excel for Python" - it helps us organize and analyze data
        # We use it to process and transform our network data
        "pandas>=2.2.0",
        
        # numpy: This provides mathematical functions and array operations
        # It's like a "calculator library" for complex math operations
        # Many other libraries (like pandas) depend on numpy
        "numpy>=1.26.3",
        
        # networkx: This is specifically for working with graph data
        # It's like a "graph toolkit" with functions for analyzing networks
        # We use it for calculating network properties and layouts
        "networkx>=3.2.1"
    ],
    
    # PYTHON VERSION REQUIREMENT - Which Python versions can run our software
    # -------------------------------------------------------------------------
    
    # python_requires: This specifies the minimum Python version needed
    # ">=3.8" means our software requires Python 3.8 or newer
    # This is important because newer Python versions have features we use
    python_requires=">=3.8",
) 