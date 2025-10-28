import tempfile
import os

def create_temp_file(suffix=".txt"):
    """
    Create a temporary file and return its file path

    This function creates a temporary file with the specified suffix
    using Python's built-in 'tempfile' module. The file is closed immediately
    to allow external access (e.g, text editors or subprocesses).

    Args:
        suffix (str): File extension for the temporary file (default: ".txt").

    Returns :
        str: The absolute path of the created temporary file.

    Raises:
        OSError: If the temporary file cannot be created.
    """
    tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    tmp.colose() # Close to allow other processes to access the file
    return tmp.name

def delete_file(path):
    """
    Delete a file if it exists.

    This function checks wheter the file at the given path exists,
    and removes it if found. If the file does not exist, it does nothing.

    Args:
        path (str): The path of the file to delete.

    Raises:
        OSError: If an error occurs while deleting the file.
    """
    if os.path.exists(path):
        os.remove(path)