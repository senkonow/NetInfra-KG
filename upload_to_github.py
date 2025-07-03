#!/usr/bin/env python3
"""
Automated GitHub Upload Script for Network Infrastructure Knowledge Graph
"""
import os
import subprocess
import sys
from pathlib import Path


def run_command(command, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode


def check_git_installed():
    """Check if Git is installed"""
    stdout, stderr, returncode = run_command("git --version", check=False)
    if returncode != 0:
        print("❌ Git is not installed. Please install Git first:")
        print("   - macOS: brew install git")
        print("   - Windows: https://git-scm.com/download/win")
        print("   - Linux: sudo apt install git")
        return False
    print(f"✅ Git detected: {stdout}")
    return True


def check_github_cli():
    """Check if GitHub CLI is available"""
    stdout, stderr, returncode = run_command("gh --version", check=False)
    return returncode == 0


def get_user_input():
    """Get repository details from user"""
    print("\n📝 Repository Setup")
    print("-" * 30)
    
    repo_name = input("Repository name [network-infrastructure-kg]: ").strip()
    if not repo_name:
        repo_name = "network-infrastructure-kg"
    
    description = input("Repository description [Neo4j Knowledge Graph for Network Infrastructure]: ").strip()
    if not description:
        description = "Neo4j Knowledge Graph for Network Infrastructure Topology - LLM Ready"
    
    is_public = input("Make repository public? [Y/n]: ").strip().lower()
    public = is_public != 'n'
    
    github_username = input("Your GitHub username: ").strip()
    if not github_username:
        print("❌ GitHub username is required")
        return None
    
    return {
        'repo_name': repo_name,
        'description': description,
        'public': public,
        'username': github_username
    }


def initialize_git():
    """Initialize git repository"""
    print("\n🔧 Initializing Git repository...")
    
    # Check if already a git repository
    if os.path.exists('.git'):
        print("📁 Git repository already exists")
        return True
    
    commands = [
        "git init",
        "git add .",
        'git commit -m "Initial commit: Neo4j Knowledge Graph for Network Infrastructure"',
        "git branch -M main"
    ]
    
    for cmd in commands:
        print(f"   Running: {cmd}")
        stdout, stderr, returncode = run_command(cmd)
        if returncode != 0:
            print(f"❌ Command failed: {cmd}")
            print(f"   Error: {stderr}")
            return False
        elif stdout:
            print(f"   {stdout}")
    
    print("✅ Git repository initialized")
    return True


def upload_with_github_cli(repo_info):
    """Upload using GitHub CLI"""
    print("\n🚀 Creating repository with GitHub CLI...")
    
    visibility = "--public" if repo_info['public'] else "--private"
    cmd = f'gh repo create {repo_info["repo_name"]} {visibility} --description "{repo_info["description"]}" --source=. --remote=origin --push'
    
    print(f"   Running: {cmd}")
    stdout, stderr, returncode = run_command(cmd)
    
    if returncode == 0:
        print("✅ Repository created and uploaded successfully!")
        print(f"🌐 Repository URL: https://github.com/{repo_info['username']}/{repo_info['repo_name']}")
        return True
    else:
        print(f"❌ GitHub CLI upload failed: {stderr}")
        return False


def upload_with_git(repo_info):
    """Upload using standard git commands"""
    print("\n🚀 Uploading to GitHub with Git...")
    
    repo_url = f"https://github.com/{repo_info['username']}/{repo_info['repo_name']}.git"
    
    print(f"📋 Manual steps required:")
    print(f"   1. Go to https://github.com/new")
    print(f"   2. Create repository: {repo_info['repo_name']}")
    print(f"   3. Description: {repo_info['description']}")
    print(f"   4. Visibility: {'Public' if repo_info['public'] else 'Private'}")
    print(f"   5. DON'T initialize with README, .gitignore, or license")
    
    input("\nPress Enter after creating the repository on GitHub...")
    
    commands = [
        f"git remote add origin {repo_url}",
        "git push -u origin main"
    ]
    
    for cmd in commands:
        print(f"   Running: {cmd}")
        stdout, stderr, returncode = run_command(cmd)
        if returncode != 0:
            print(f"❌ Command failed: {cmd}")
            print(f"   Error: {stderr}")
            if "Authentication" in stderr or "denied" in stderr:
                print("\n🔐 Authentication Help:")
                print("   - Use Personal Access Token as password")
                print("   - Generate at: https://github.com/settings/tokens")
                print("   - Select 'repo' permissions")
            return False
        elif stdout:
            print(f"   {stdout}")
    
    print("✅ Repository uploaded successfully!")
    print(f"🌐 Repository URL: https://github.com/{repo_info['username']}/{repo_info['repo_name']}")
    return True


def print_next_steps(repo_info):
    """Print next steps after successful upload"""
    repo_url = f"https://github.com/{repo_info['username']}/{repo_info['repo_name']}"
    
    print(f"\n🎉 Success! Your project is now on GitHub")
    print("=" * 50)
    print(f"📍 Repository: {repo_url}")
    print(f"📋 Clone URL: {repo_url}.git")
    print(f"🐛 Issues: {repo_url}/issues")
    print(f"📚 Wiki: {repo_url}/wiki")
    
    print(f"\n📋 Recommended Next Steps:")
    print(f"   1. Visit your repository: {repo_url}")
    print(f"   2. Add repository topics: neo4j, knowledge-graph, llm")
    print(f"   3. Star your own repository ⭐")
    print(f"   4. Share with the community!")
    
    print(f"\n🔄 Future Updates:")
    print(f"   git add .")
    print(f"   git commit -m \"Your update description\"")
    print(f"   git push")


def main():
    """Main upload function"""
    print("🚀 GitHub Upload Assistant")
    print("=" * 40)
    print("This script will help you upload your Neo4j Knowledge Graph project to GitHub")
    
    # Check prerequisites
    if not check_git_installed():
        return
    
    has_gh_cli = check_github_cli()
    if has_gh_cli:
        print("✅ GitHub CLI detected - will use for easier upload")
    else:
        print("📝 GitHub CLI not found - will use standard Git workflow")
    
    # Get repository information
    repo_info = get_user_input()
    if not repo_info:
        return
    
    # Initialize git
    if not initialize_git():
        return
    
    # Upload to GitHub
    success = False
    if has_gh_cli:
        success = upload_with_github_cli(repo_info)
        if not success:
            print("\n🔄 Falling back to standard Git upload...")
            success = upload_with_git(repo_info)
    else:
        success = upload_with_git(repo_info)
    
    if success:
        print_next_steps(repo_info)
    else:
        print("\n❌ Upload failed. Please check the detailed instructions in:")
        print("   github_upload_instructions.md")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Upload cancelled by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check github_upload_instructions.md for manual upload steps") 