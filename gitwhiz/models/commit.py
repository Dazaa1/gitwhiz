import subprocess
from .constants import VALID_COMMIT_TYPES

class Commit:
    def __init__(self):
        pass

    def validate_message(self, message):
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
        valide_message = self.validate_message(message)
        if valide_message:
            message_arr = message.split(":")
            return {
                "type": message_arr[0].split("(")[0].strip(),
                "Description": message_arr[1].strip()
            }
