#!/bin/bash
# GitHub Helper Script for IEEE 118-Bus System Repository
# Usage: ./github_helper.sh [command]
# Commands:
#   status - Show git status
#   push - Push changes to GitHub
#   pull - Pull changes from GitHub
#   commit - Commit changes (requires message)
#   log - Show commit history
#   url - Show repository URL

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Repository URL
REPO_URL="https://github.com/hrid0yislam/IEEE118Bus"

# Function to show status
show_status() {
    echo "=== Git Status ==="
    git status
}

# Function to push changes
push_changes() {
    echo "=== Pushing changes to GitHub ==="
    git push origin main
    echo "Visit your repository at: $REPO_URL"
}

# Function to pull changes
pull_changes() {
    echo "=== Pulling changes from GitHub ==="
    git pull origin main
}

# Function to commit changes
commit_changes() {
    if [ -z "$1" ]; then
        echo "Error: Commit message is required"
        echo "Usage: ./github_helper.sh commit \"Your commit message\""
        exit 1
    fi
    
    echo "=== Committing changes ==="
    git add .
    git commit -m "$1"
    echo "Changes committed. Use './github_helper.sh push' to push to GitHub."
}

# Function to show commit history
show_log() {
    echo "=== Commit History ==="
    git log --oneline --graph --decorate -n 10
}

# Function to show repository URL
show_url() {
    echo "=== Repository URL ==="
    echo "Your repository is available at: $REPO_URL"
    echo "To clone this repository elsewhere, use:"
    echo "git clone $REPO_URL"
}

# Main script logic
case "$1" in
    status)
        show_status
        ;;
    push)
        push_changes
        ;;
    pull)
        pull_changes
        ;;
    commit)
        commit_changes "$2"
        ;;
    log)
        show_log
        ;;
    url)
        show_url
        ;;
    *)
        echo "IEEE 118-Bus System GitHub Helper"
        echo "Usage: ./github_helper.sh [command]"
        echo ""
        echo "Available commands:"
        echo "  status  - Show git status"
        echo "  push    - Push changes to GitHub"
        echo "  pull    - Pull changes from GitHub"
        echo "  commit  - Commit changes (requires message)"
        echo "  log     - Show commit history"
        echo "  url     - Show repository URL"
        echo ""
        echo "Example:"
        echo "  ./github_helper.sh commit \"Update README with installation instructions\""
        ;;
esac 