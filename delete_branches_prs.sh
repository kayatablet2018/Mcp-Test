#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
MAIN_BRANCH="main"

# --- Functions ---

# Function to confirm an action
confirm_action() {
    read -p "Are you absolutely sure you want to proceed? This action is irreversible. (y/N): " response
    if [[ "$response" != "y" && "$response" != "Y" ]]; then
        echo "Action cancelled."
        exit 0
    fi
}

# --- Main Script ---

echo "WARNING: This script will delete all local and remote Git branches except '$MAIN_BRANCH'."
echo "It will also attempt to close open Pull Requests using GitHub CLI (gh)."
echo "PLEASE ENSURE YOU HAVE A BACKUP OR ARE AWARE OF THE IRREVERSIBLE CONSEQUENCES."
confirm_action

# Ensure we are on the main branch before attempting to delete other local branches
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "$MAIN_BRANCH" ]; then
    echo "Currently on branch '$CURRENT_BRANCH'. Switching to '$MAIN_BRANCH' for safe deletion."
    git checkout "$MAIN_BRANCH" || { echo "ERROR: Could not checkout '$MAIN_BRANCH'. Please resolve manually."; exit 1; }
fi

echo ""
echo "--- Deleting Local Branches ---"
# Get all local branches except main
# Filter out current branch just in case, though it should be main now
LOCAL_BRANCHES=$(git branch --format="%(refname:short)" | grep -v "^$MAIN_BRANCH$")

if [ -z "$LOCAL_BRANCHES" ]; then
    echo "No local branches found to delete (excluding '$MAIN_BRANCH')."
else
    echo "The following local branches will be deleted:"
    echo "$LOCAL_BRANCHES"
    read -p "Confirm deletion of these local branches? (y/N): " local_confirm
    if [[ "$local_confirm" == "y" || "$local_confirm" == "Y" ]]; then
        echo "$LOCAL_BRANCHES" | xargs -n 1 git branch -D || true # Use || true to avoid script exit on branch not found/already deleted
        echo "Local branches deleted successfully."
    else
        echo "Local branch deletion cancelled."
    fi
fi

echo ""
echo "--- Deleting Remote Branches ---"
# Fetch latest remote info
git fetch --all --prune || { echo "WARNING: git fetch failed. Remote branch deletion might be incomplete."; }

# Get all remote branches except main
# Filter out HEAD -> origin/main
REMOTE_BRANCHES=$(git branch -r --format="%(refname:short)" | grep -v "origin/$MAIN_BRANCH$" | grep -v "HEAD ->" | sed 's/origin\///')

if [ -z "$REMOTE_BRANCHES" ]; then
    echo "No remote branches found to delete (excluding 'origin/$MAIN_BRANCH')."
else
    echo "The following remote branches will be deleted:"
    echo "$REMOTE_BRANCHES"
    read -p "Confirm deletion of these remote branches? (y/N): " remote_confirm
    if [[ "$remote_confirm" == "y" || "$remote_confirm" == "Y" ]]; then
        # Delete remote branches
        echo "$REMOTE_BRANCHES" | xargs -n 1 -I {} git push origin --delete {} || true
        echo "Remote branches deleted successfully."
    else
        echo "Remote branch deletion cancelled."
    fi
fi

echo ""
echo "--- Closing Pull Requests ---"
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) not found. Skipping Pull Request operations."
    echo "Please install gh to manage Pull Requests: https://cli.github.com/"
else
    echo "Attempting to close open Pull Requests using GitHub CLI..."
    # List open PRs
    # Using gh pr list --state open --limit 100 --json number,title for robust parsing
    OPEN_PRS_JSON=$(gh pr list --state open --limit 100 --json number,title 2>/dev/null)

    if [ -z "$OPEN_PRS_JSON" ] || [ "$OPEN_PRS_JSON" == "[]" ]; then
        echo "No open Pull Requests found."
    else
        PR_NUMBERS=""
        if command -v jq &> /dev/null; then
            PR_NUMBERS=$(echo "$OPEN_PRS_JSON" | jq -r '.[].number')
            echo "The following open Pull Requests will be closed:"
            echo "$OPEN_PRS_JSON" | jq -r '.[] | "\(.number) - \(.title)"'
        else
            echo "jq not found. Listing PRs by number only."
            PR_NUMBERS=$(echo "$OPEN_PRS_JSON" | grep -oP '"number":\K[0-9]+' | sort -u)
            echo "The following open Pull Requests will be closed (numbers only):"
            echo "$PR_NUMBERS"
        fi

        if [ -z "$PR_NUMBERS" ]; then
            echo "No parseable open Pull Requests found."
        else
            read -p "Confirm closing of these open Pull Requests? (y/N): " pr_open_confirm
            if [[ "$pr_open_confirm" == "y" || "$pr_open_confirm" == "Y" ]]; then
                for PR_NUM in $PR_NUMBERS; do
                    echo "Closing PR #$PR_NUM..."
                    gh pr close "$PR_NUM" --confirm || true
                done
                echo "Open Pull Requests closed successfully."
            else
                echo "Open Pull Request closing cancelled."
            fi
        fi
    fi

    echo ""
    echo "Merged Pull Requests are already in a closed state. This script focuses on closing *open* Pull Requests."
    echo "Deleting merged PR history is not a standard Git/GitHub CLI operation."
fi

echo ""
echo "--- Cleanup ---"
echo "Running git remote prune origin to remove any stale remote-tracking branches."
git remote prune origin || { echo "WARNING: git remote prune origin failed. Some stale remote-tracking branches might remain."; }

echo "Script finished successfully."
