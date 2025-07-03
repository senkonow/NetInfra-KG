from setuptools import setup, find_packages

setup(
    name="network-infrastructure-kg",
    version="0.1.0",
    description="Neo4j Knowledge Graph for Network Infrastructure Topology",
    author="Infrastructure Team",
    packages=find_packages(),
    install_requires=[
        "neo4j>=5.17.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.6.1",
        "fastapi>=0.109.2",
        "uvicorn>=0.27.1",
        "requests>=2.31.0",
        "pandas>=2.2.0",
        "numpy>=1.26.3",
        "networkx>=3.2.1"
    ],
    python_requires=">=3.8",
) 