import subprocess
from .constants import VALID_COMMIT_TYPES

class Commit:
    """
    A class for validating, creating, and parsing git commit messages.
    
    Provides methods to validate commit message format, create commits with
    validated messages, and parse commit messages into structured components.
    """
    def __init__(self):
        """
        Initialize a Commit instance.
        
        Prepares the Commit object for handling git commit operations.
        """
        pass

    def validate_message(self, message):
        """
        Validate that a commit message follows the expected format.
        
        Checks that the message contains a valid commit type (from VALID_COMMIT_TYPES),
        followed by a colon and a non-empty description. The type may optionally
        include a scope in parentheses (e.g., "feat(scope)").
        
        Args:
            message (str): The commit message to validate.
        
        Returns:
            bool: True if the message is valid, False otherwise.
        """
        parts = message.split(":")
    
        if len(parts) < 2:
            return False
    
        type_part = parts[0]
        description = parts[1].strip()
        

        type_only = type_part.split("(")[0].strip()
        
        if type_only in VALID_COMMIT_TYPES and len(description) > 0:
            return True
        else:
            return False

    def create_commit(self, message):
        """
        Create a git commit with the provided message.
        
        Validates the commit message format before creating the commit.
        If validation passes, executes 'git commit' with the message.
        If validation fails, prints an error message.
        
        Args:
            message (str): The commit message to use for the new commit.
        
        Returns:
            bool: True if the commit was successfully created, None otherwise.
        """
        valide_message = self.validate_message(message)
        if valide_message:
            subprocess.run(
                ["git", "commit", "-m", message],
                capture_output=True,
                text=True,
                check=True
            )
            return True

        else:
            print("Invalid commit format")

    def parse_message(self, message):
        """
        Parse a commit message into structured components.
        
        Extracts the commit type and description from a validated commit message.
        Returns a dictionary containing the type and description if the message
        is valid, otherwise returns None implicitly.
        
        Args:
            message (str): The commit message to parse.
        
        Returns:
            dict: A dictionary with keys 'type' and 'Description' if valid, None otherwise.
        """
        valide_message = self.validate_message(message)
        if valide_message:
            message_arr = message.split(":")
            return {
                "type": message_arr[0].split("(")[0].strip(),
                "Description": message_arr[1].strip()
            }