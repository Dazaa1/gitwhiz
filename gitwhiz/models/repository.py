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
        pass

    def un_command(self, command):
        pass


    def is_git_repo(self):
        pass