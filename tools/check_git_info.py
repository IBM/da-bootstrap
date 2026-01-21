#!/usr/bin/env python3
"""
Git Information Detection Script
Checks for Git repository and version tags in a specified directory.
"""

import subprocess
import sys
import os
import json


def run_command(cmd, cwd=None):
    """Execute a shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip()
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Command timed out"
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }


def check_git_repository(directory):
    """Check if directory is a Git repository and get remote info."""
    result = run_command("git remote -v", cwd=directory)
    
    if result["success"] and result["output"]:
        remotes = []
        for line in result["output"].split('\n'):
            if line.strip():
                remotes.append(line)
        return {
            "is_git_repo": True,
            "remotes": remotes
        }
    else:
        return {
            "is_git_repo": False,
            "remotes": []
        }


def check_version_tags(directory):
    """Check for semantic version tags in the Git repository."""
    result = run_command("git tag -l | grep -E '^v?[0-9]+\\.[0-9]+\\.[0-9]+$'", cwd=directory)
    
    if result["success"] and result["output"]:
        tags = [tag.strip() for tag in result["output"].split('\n') if tag.strip()]
        return {
            "has_version_tags": True,
            "tags": tags,
            "count": len(tags)
        }
    else:
        return {
            "has_version_tags": False,
            "tags": [],
            "count": 0
        }


def main():
    """Main function to check Git information."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python check_git_info.py <directory_path> [--summary]"
        }, indent=2))
        sys.exit(1)
    
    directory = sys.argv[1]
    summary_mode = "--summary" in sys.argv
    
    if not os.path.isdir(directory):
        print(json.dumps({
            "error": f"Directory not found: {directory}"
        }, indent=2))
        sys.exit(1)
    
    # Check Git repository
    git_info = check_git_repository(directory)
    
    # Check version tags (only if it's a Git repo)
    if git_info["is_git_repo"]:
        tag_info = check_version_tags(directory)
    else:
        tag_info = {
            "has_version_tags": False,
            "tags": [],
            "count": 0
        }
    
    # Combine results
    if summary_mode:
        # Minimal output for Bob
        result = {
            "directory": directory,
            "is_git_repo": git_info["is_git_repo"],
            "has_version_tags": tag_info["has_version_tags"],
            "tag_count": tag_info["count"]
        }
    else:
        # Full detailed output
        result = {
            "directory": directory,
            "git_repository": git_info,
            "version_tags": tag_info
        }
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

# Made with Bob
