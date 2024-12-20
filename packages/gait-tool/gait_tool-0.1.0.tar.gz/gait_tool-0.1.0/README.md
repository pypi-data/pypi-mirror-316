# Gait（g-AI-t）: An AI enhanced git command line utility

## Table of Contents
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Basic Installation and Configuration](#basic-installation-and-configuration)
  - [Installing GitHub CLI](#installing-github-cli)
- [Usage](#usage)
  - [Basic Git Commands](#basic-git-commands)
  - [AI-Generated Commits](#ai-generated-commits)
  - [AI-Generated Pull Requests](#ai-generated-pull-requests)
  - [Linear Integration and TODO Processing](#linear-integration-and-todo-processing)
- [Project Structure](#project-structure)


## Installation

### Prerequisites
- Python 3.7 or later ([Download from python.org](https://www.python.org/downloads/))
  ```bash
  python3 --version  # Verify Python installation
  ```
- Git
  ```bash
  git --version    # Verify Git installation
  ```
- GitHub CLI (for PR features)
- OpenAI (requires API key)
- Linear (requires API key and team ID)

### BasicInstallation and Configuration
For macOS:
1. Clone the repository and install:
   ```bash
   # Clone the repository
   git clone https://github.com/EmpyreanTechnologiesInc/gait.git


   # Navigate to directory and install
   cd gait
   pip install -e .
   
   # Verify installation
   gait --version # should display the git version number
   ```

2. Configure AI Features

   ```bash
   # Find the .env.example file in gait directory 
   # Copy and rename it to .env
   cp .env.example .env
   
   # Open the .env file in your preferred editor
   nano .env   # or vim .env, code .env, etc.
   
   # Add your OpenAI API key to .env file
   OPENAI_API_KEY=your_api_key_here
   
   # (Optional) Configure AI model
   OPENAI_MODEL=gpt-4o-mini  # Default model
   
   # Test your OpenAI API connection
   gait test-api # If successful, you'll see: "API connection successful!"
   ```

### Installing GitHub CLI
For macOS:
   ```bash
   # Install Homebrew if you haven't
   pip install brew
   
   # Use brew to install GitHub CLI
   brew install gh
   ```

After installation, authenticate with GitHub:
```bash
gh auth login # Follow the prompts to complete the authentication process
```

## Usage

### Basic Git Commands
Any git command you know can be used with gait:

```bash
# Basic git commands
gait status
gait add .
gait commit -m "your message"
gait push

# All git commands are supported
gait branch -a
gait checkout -b feature/new-branch
gait merge main
```

### Automatically Generate Git Commits with AI

The `gait commit --ai` command analyzes your staged changes and uses AI to generate a descriptive commit message. This feature helps maintain consistent and informative commit messages across your project.

```bash
# Stage your changes first
gait add .

# Generate AI commit message
gait commit --ai

# You'll be prompted to:
# 1. Review the generated message
# 2. Accept (y), reject (n), or edit (e) the message
# 3. Once accepted or edited, 'git commit -m "<message>"' will be executed automatically
```

### AI-Generated Pull Requests
The `gait pr create --ai` command analyzes your branch changes and uses AI to generate a descriptive pull request title and body. This feature helps create comprehensive and well-structured pull requests. All standard `gh pr create` options (like `--draft`, `--base`, etc.) are supported.

```bash
# Make sure your changes are committed and pushed
gait push

# Generate AI pull request
gait pr create --ai                           # Basic AI-generated PR
# Other options
gait pr create --ai --draft                   # Create as draft PR
gait pr create --ai --base main               # Set target branch

# You'll be prompted to:
# 1. Review the generated PR title and body
# 2. Accept (y), reject (n), or edit (e) the content
# 3. Once accepted or edited, the PR will be created automatically using GitHub CLI
```

### Linear Integration and TODO Processing
When creating a pull request with `gait pr create --ai`, the tool automatically processes TODO comments in your changes:

1. For new TODOs:
   - Creates corresponding Linear issues
   - Updates the TODO comment with the Linear issue ID
   - Example: `# TODO: Add tests` becomes `# TODO(ENG-123): Add tests`

2. For removed TODOs:
   - Automatically marks the corresponding Linear issue as "Done"
   - Example: When you remove `# TODO(ENG-123): Add tests`, issue ENG-123 will be marked as completed

```bash
# Example TODO comment format:
# TODO:Implement error handling
# TODO(context): Add unit tests

# When creating a PR:
# 1. New TODOs will be converted to Linear issues
#    # TODO(ENG-123): Implement error handling
# 2. Removed TODOs will be marked as done in Linear
```

To use this feature, configure Linear in your `.env` file:
```bash
LINEAR_API_KEY=your_linear_api_key
LINEAR_TEAM_ID=your_team_id
LINEAR_PROJECT_ID=your_project_id
```
- Team ID and Project ID can be found on the Linear webpage:
  1. Press `Cmd/Ctrl + K`
  2. Find "Copy model UUID"
  3. select the ID to copy

- API Key can be found in Settings > API

## Project Structure
```
gait/
├── src/
│   └── gait/
│       ├── __init__.py
│       ├── main.py
│       ├── git_wrapper.py
│       ├── github_wrapper.py
│       ├── ai_commit.py
│       ├── ai_pr.py
│       ├── linear_client.py
│       └── utils.py
├── README.md
├── LICENSE
├── setup.py
├── pyproject.toml
├── requirements.txt
├── .gitignore
└── .env.example
```