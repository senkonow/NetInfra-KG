#!/usr/bin/env python3
"""
Installation and Setup Script for Network Infrastructure Knowledge Graph
"""
import os
import sys
import subprocess
import time
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)


def check_neo4j_connection():
    """Check if Neo4j is accessible"""
    print("\n🔍 Checking Neo4j connection...")
    try:
        from kg.database import Neo4jKnowledgeGraph
        kg = Neo4jKnowledgeGraph()
        kg.close()
        print("✅ Neo4j connection successful")
        return True
    except Exception as e:
        print(f"⚠️  Neo4j connection failed: {e}")
        return False


def setup_neo4j_with_docker():
    """Setup Neo4j using Docker"""
    print("\n🐳 Setting up Neo4j with Docker...")
    try:
        # Check if Docker is available
        subprocess.check_call(["docker", "--version"], stdout=subprocess.DEVNULL)
        
        # Stop any existing Neo4j container
        subprocess.run(["docker", "stop", "neo4j-kg"], stderr=subprocess.DEVNULL)
        subprocess.run(["docker", "rm", "neo4j-kg"], stderr=subprocess.DEVNULL)
        
        # Start Neo4j container
        cmd = [
            "docker", "run", "-d",
            "--name", "neo4j-kg",
            "-p", "7474:7474",
            "-p", "7687:7687",
            "-e", "NEO4J_AUTH=neo4j/password",
            "-v", "neo4j_data:/data",
            "neo4j:latest"
        ]
        
        subprocess.check_call(cmd)
        print("✅ Neo4j Docker container started")
        
        # Wait for Neo4j to be ready
        print("⏳ Waiting for Neo4j to be ready...")
        for i in range(30):
            if check_neo4j_connection():
                return True
            time.sleep(2)
            print(f"   Waiting... ({i+1}/30)")
        
        print("❌ Neo4j failed to start within timeout")
        return False
        
    except subprocess.CalledProcessError:
        print("❌ Docker not available or command failed")
        return False


def create_env_file():
    """Create environment configuration file"""
    env_content = """# Neo4j Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# Optional: Neo4j Database Name (Neo4j 4.0+)
NEO4J_DATABASE=neo4j

# Application Configuration
LOG_LEVEL=INFO
ENVIRONMENT=development

# Data Generation Settings
GENERATE_SAMPLE_DATA=true
SWITCH_COUNT=3
PORTS_PER_SWITCH=24
VLAN_COUNT=10
SERVER_COUNT=5
VMS_PER_SERVER=10
PODS_PER_VM=100
"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Created .env configuration file")
    else:
        print("📄 .env file already exists")


def run_demo():
    """Run the main demo"""
    print("\n🚀 Running the knowledge graph demo...")
    try:
        subprocess.check_call([sys.executable, "main.py"])
        print("✅ Demo completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Demo failed: {e}")
        sys.exit(1)


def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("   1. Open Neo4j Browser: http://localhost:7474")
    print("      - Username: neo4j")
    print("      - Password: password")
    print("   2. Explore the generated knowledge graph")
    print("   3. Try the exported data files:")
    print("      - infrastructure_kg_export.json")
    print("      - infrastructure_kg_export.txt")
    print("   4. Modify the code for your use case")
    print("\n🔧 Useful Commands:")
    print("   - Run demo again: python main.py")
    print("   - Clear database: python -c \"from kg.database import Neo4jKnowledgeGraph; kg = Neo4jKnowledgeGraph(); kg.clear_database()\"")
    print("   - Stop Neo4j Docker: docker stop neo4j-kg")
    print("   - Start Neo4j Docker: docker start neo4j-kg")


def main():
    """Main installation and setup function"""
    print("🏗️  Network Infrastructure Knowledge Graph - Installation & Setup")
    print("=" * 70)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create environment file
    create_env_file()
    
    # Check Neo4j connection
    if not check_neo4j_connection():
        print("\n🐳 Neo4j not accessible. Attempting to start with Docker...")
        if not setup_neo4j_with_docker():
            print("\n❌ Failed to setup Neo4j. Please install Neo4j manually:")
            print("   1. Download from: https://neo4j.com/download/")
            print("   2. Or use Docker: docker run -p7474:7474 -p7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest")
            print("   3. Then run: python main.py")
            return
    
    # Run the demo
    run_demo()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main() 