import logging
import os
import tempfile

def create_temp_file(suffix=".txt")->str:
    """
    Create a temporary file and return its file path

    The file is created in the system's temporary using Python's
    built-in 'tempfile' module. It is closed immediately to allow access by
    external processes or tools

    Args:
        suffix (str): File extension for the temporary file (default: ".txt").

    Returns :
        str: Absolute path to the created temporary file.

    Raises:
        ValueError: If the given suffix is invalid.
        OSError: If the temporary file cannot be created.
    """
    if not suffix.startswith(".") or "/" in suffix or "\\" in suffix:
        raise ValueError("Invalid file suffix")
    
    tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    tmp.close() # Close to allow other processes to access the file
    return tmp.name

def delete_file(path)->None:
    """
    Delete a temporary file if it exists and is located in the system temp directory.

    This function ensure the only files inside the system's temporary directory
    are deletes. Non-temporary file are ignored for safety.

    Args:
        path (str): Path of the file to delete.

    Raises:
        OSError: If an error occurs during file deletion.
    """
    try:
        temp_dir = os.path.abspath(tempfile.gettempdir())
        abs_path = os.path.abspath(path)

        if not abs_path.startswith(temp_dir):
            logging.warning("Deletion blocked for non-temporary file: %s", abs_path)
            return
        
        if os.path.exists(abs_path) and os.path.isfile(abs_path):
            os.remove(abs_path)
        else:
            logging.warning("File not found or invalid path: %s", abs_path)

    except OSError as e:
        logging.warning("Failed to delete %s (%s)", path, e)