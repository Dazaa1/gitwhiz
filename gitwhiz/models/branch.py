import subprocess
from datetime import datetime

class Branch:
    def __init__(self):
        pass

    def create_branch(self, name):
        subprocess.run(
            ["git", "branch", name],
            capture_output=True,
            text=True,
            check=True
        )

    def switch_branch(self, name):
        subprocess.run(
            ["git", "switch", name],
            capture_output=True,
            text=True,
            check=True
        )

    def delete_branch(self, name):
        subprocess.run(
            ["git", "branch", "-d", name],
            capture_output=True,
            text=True,
            check=True
        )

    def get_all_branches(self):
        result = subprocess.run(
            ["git", "branch"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')

    def is_merged(self, name, base_branch=None):
        """Check if a branch is merged into the base branch."""
        if base_branch is None:
            # Get the default branch (main or master)
            base_branch = self._get_default_branch()
        
        result = subprocess.run(
            ["git", "branch", "--merged", base_branch],
            capture_output=True,
            text=True,
            check=True
        )
        return name in result.stdout

    def _get_default_branch(self):
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "origin/HEAD"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().split('/')[-1]
        return "main"