import subprocess

class Repository:
    """
        A class that talk to git using subprocess
    """
    def __init__(self):
        pass


    def get_status(self):
        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout

    def get_current_branch(self):
        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout

    def get_all_branches(self):
        result = subprocess.run(
            ["git", "branch", "-a"],
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout


    def is_git_repo(self):
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout