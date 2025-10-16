import subprocess

class Repository:
    """
    A class that talks to git using subprocess.
    
    Provides methods to interact with git repositories by executing
    git commands and returning their output.
    """
    def __init__(self):
        """
        Initialize a Repository instance.
        
        This constructor prepares the Repository object for use with git commands.
        """
        pass


    def get_status(self):
        """
        Get the current status of the git repository.
        
        Executes 'git status' command and returns the status output,
        including information about staged, unstaged, and untracked files.
        
        Returns:
            str: The output of the git status command.
        """
        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout

    def get_current_branch(self):
        """
        Get the name of the current branch.
        
        Executes 'git status' command and returns the output which includes
        the current branch information.
        
        Returns:
            str: The output of the git status command showing current branch.
        """
        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout

    def get_all_branches(self):
        """
        Get a list of all branches in the repository.
        
        Executes 'git branch -a' command to retrieve both local and remote branches.
        
        Returns:
            str: The output of the git branch command listing all branches.
        """
        result = subprocess.run(
            ["git", "branch", "-a"],
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout


    def is_git_repo(self):
        """
        Check if the current directory is inside a git repository.
        
        Executes 'git rev-parse --is-inside-work-tree' command to determine
        whether the current location is within a git working directory.
        
        Returns:
            str: The output indicating whether inside a git repository.
        """
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout