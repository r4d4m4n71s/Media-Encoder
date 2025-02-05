import json
from __init__ import get_logger

class JsonLoader:

    _instances = {}  # Dictionary to store instances per file_path

    def __new__(cls, file_path):
        # Check if an instance for this file_path already exists
        if file_path not in cls._instances:
            # Create a new instance and store it in the dictionary
            cls._instances[file_path] = super(JsonLoader, cls).__new__(cls)
            # Initialize the instance with the file_path
            cls._instances[file_path]._file_path = file_path
        return cls._instances[file_path]

    def __init__(self, file_path):
        # Initialization logic (if any)
        pass

    def load(self):
        """Load JSON data from the file associated with this instance."""
        
        logger = get_logger(__name__)

        try:
            with open(self._file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            logger.error(f"File not found: {self._file_path}")
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in file: {self._file_path}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")        