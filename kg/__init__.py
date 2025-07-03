# =============================================================================
# __INIT__.PY - PYTHON PACKAGE INITIALIZATION FILE
# =============================================================================
# This file tells Python that the 'kg' folder is a Python package
# Think of it like a "package label" that identifies what's inside
#
# WHAT IS A PYTHON PACKAGE?
# A Python package is like a folder full of related code files
# It's a way to organize code into logical groups
# For example, our 'kg' package contains all the code for our knowledge graph system
#
# WHY DO WE NEED THIS FILE?
# Without this file, Python wouldn't recognize the 'kg' folder as a package
# It would just be a regular folder with some Python files in it
# This file makes it possible to write: from kg import models
# Instead of having to specify the full path to each file
#
# WHAT DOES THIS FILE CONTAIN?
# Usually it contains:
# 1. Package information (version, author, description)
# 2. Import statements to make key classes/functions easily accessible
# 3. Package-level configuration or initialization code

# PACKAGE DOCUMENTATION STRING
# =============================================================================
"""
Network Infrastructure Knowledge Graph Package

This package contains all the code for building and managing a Neo4j knowledge graph
that represents network infrastructure topology. It includes:

- models.py: Data structures for network entities (switches, servers, VMs, etc.)
- database.py: Functions for connecting to and managing the Neo4j database
- data_generator.py: Tools for creating sample network data
- llm_interface.py: Interface for natural language queries using LLMs
- visualization.py: Tools for creating visual representations of the network

The package is designed to help network engineers and system administrators
understand and analyze complex network topologies through graph database technology.
"""

# PACKAGE METADATA - Information about this package
# =============================================================================
# These special variables (starting and ending with __) are called "dunder" variables
# They provide metadata about the package that Python and other tools can use

# __version__: The current version of our package
# Version numbers typically follow the pattern: MAJOR.MINOR.PATCH
# 0.1.0 means: Major version 0, Minor version 1, Patch version 0
# This indicates it's an early version (0.x.x) but functional
__version__ = "0.1.0"

# __author__: Who created this package
# This gives credit to the development team
__author__ = "Infrastructure Team"

# __description__: A short summary of what this package does
# This helps people understand the purpose of the package
__description__ = "Neo4j Knowledge Graph for Network Infrastructure Topology"

# OPTIONAL: You could add more metadata here, such as:
# __email__ = "infrastructure@company.com"
# __license__ = "MIT"
# __url__ = "https://github.com/company/network-infrastructure-kg"

# PACKAGE IMPORTS - Making key components easily accessible
# =============================================================================
# When someone imports our package, these imports make it easy to access
# the most important classes and functions without having to know the internal structure
#
# For example, instead of writing:
#   from kg.models import NetworkSwitch
# Users can write:
#   from kg import NetworkSwitch
#
# This makes our package more user-friendly and easier to use

# Note: We're not importing everything here to keep the __init__.py file clean
# and to avoid circular imports (where files import each other in a loop)
# Users can still import specific modules when they need them:
#   from kg.models import NetworkSwitch
#   from kg.database import KnowledgeGraphDB
#   from kg.visualization import NetworkVisualizer 