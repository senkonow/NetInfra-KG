# Upload to GitHub Instructions

Follow these steps to upload your Network Infrastructure Knowledge Graph project to GitHub.

## Prerequisites

1. **GitHub Account**: Make sure you have a GitHub account at [github.com](https://github.com)
2. **Git Installed**: Install Git on your system
   - Windows: Download from [git-scm.com](https://git-scm.com/)
   - macOS: `brew install git` or use Xcode Command Line Tools
   - Linux: `sudo apt install git` (Ubuntu/Debian) or `sudo yum install git` (CentOS/RHEL)

## Step 1: Create a New Repository on GitHub

1. Go to [GitHub](https://github.com) and sign in
2. Click the **"New"** button or go to [github.com/new](https://github.com/new)
3. Fill in repository details:
   - **Repository name**: `network-infrastructure-kg` (or your preferred name)
   - **Description**: `Neo4j Knowledge Graph for Network Infrastructure Topology - LLM Ready`
   - **Visibility**: Choose Public or Private
   - **DON'T** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

## Step 2: Initialize Git in Your Local Project

Open a terminal/command prompt in your project directory (`/Users/spalislamovi/Projects/KGs`) and run:

```bash
# Initialize git repository
git init

# Add all files to staging
git add .

# Make your first commit
git commit -m "Initial commit: Neo4j Knowledge Graph for Network Infrastructure"

# Set the default branch name (optional, but recommended)
git branch -M main
```

## Step 3: Connect to GitHub and Push

Replace `YOUR_USERNAME` and `YOUR_REPOSITORY_NAME` with your actual GitHub username and repository name:

```bash
# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git

# Push to GitHub
git push -u origin main
```

### Example Commands (replace with your details):
```bash
git remote add origin https://github.com/spalislamovi/network-infrastructure-kg.git
git push -u origin main
```

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```bash
# Create repository and push in one step
gh repo create network-infrastructure-kg --public --source=. --remote=origin --push
```

## Step 4: Verify Upload

1. Go to your GitHub repository URL
2. Verify all files are present:
   - `README.md`
   - `main.py`
   - `kg/` directory with all Python files
   - `requirements.txt`
   - `LICENSE`
   - `.gitignore`

## Step 5: Set Up Repository Settings (Optional)

### Add Topics/Tags
In your GitHub repository:
1. Click the gear icon next to "About"
2. Add topics: `neo4j`, `knowledge-graph`, `llm`, `network-infrastructure`, `python`, `graph-database`

### Enable GitHub Pages (Optional)
If you want to host documentation:
1. Go to Settings → Pages
2. Select source branch (usually `main`)
3. Your documentation will be available at `https://YOUR_USERNAME.github.io/YOUR_REPOSITORY_NAME`

## Troubleshooting

### Authentication Issues
If you get authentication errors:

1. **Use Personal Access Token** (recommended):
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` permissions
   - Use token as password when prompted

2. **Or use SSH** (alternative):
   ```bash
   # Generate SSH key
   ssh-keygen -t ed25519 -C "your_email@example.com"
   
   # Add to GitHub: Settings → SSH and GPG keys
   # Then use SSH URL instead:
   git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
   ```

### Large Files
If you have large files (>100MB), consider using Git LFS:
```bash
git lfs install
git lfs track "*.json"  # for large export files
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

## Future Updates

To update your GitHub repository after making changes:

```bash
# Stage changes
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push
```

## Project Structure in GitHub

Your repository should have this structure:
```
network-infrastructure-kg/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── config.py
├── main.py
├── install_and_run.py
├── github_upload_instructions.md
└── kg/
    ├── __init__.py
    ├── models.py
    ├── database.py
    ├── data_generator.py
    └── llm_interface.py
```

## Next Steps After Upload

1. **Update README.md** with your GitHub repository link
2. **Create Issues** for future enhancements
3. **Set up GitHub Actions** for CI/CD (optional)
4. **Add contributors** if working with a team
5. **Create releases** when you reach milestones

## Example Repository URLs

Once uploaded, your project URLs will be:
- **Repository**: `https://github.com/YOUR_USERNAME/network-infrastructure-kg`
- **Clone URL**: `https://github.com/YOUR_USERNAME/network-infrastructure-kg.git`
- **Issues**: `https://github.com/YOUR_USERNAME/network-infrastructure-kg/issues`
- **Wiki**: `https://github.com/YOUR_USERNAME/network-infrastructure-kg/wiki`

---

**Need Help?** 
- GitHub Docs: [docs.github.com](https://docs.github.com)
- Git Docs: [git-scm.com/doc](https://git-scm.com/doc) 