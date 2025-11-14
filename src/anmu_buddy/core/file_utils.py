import logging
import os
import tempfile
import sys
import subprocess

def _create_temp_file(suffix=".txt")->str:
    """
    Create a temporary file and return its absolute file path.

    The file is created in the system's temporary directory using Python's
    built-in 'tempfile' module. It is immediately closed so external processes
    or tools can access it.

    Args:
        suffix (str): File extension for the temporary file (default: ".txt").

    Returns:
        str: Absolute path to the created temporary file.

    Raises:
        ValueError: If the suffix is invalid.
        OSError: If the temporary file cannot be created.
    """
    if not suffix.startswith(".") or "/" in suffix or "\\" in suffix:
        raise ValueError("Invalid file suffix")
    
    tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    tmp.close() # Close to allow other processes to access the file
    return tmp.name

def open_temp_file_for_editing(suffix=".txt", editor=None) -> str:
    """
    Create a temporary file, open it in a text editor, wait until closed,
    then return the content of the file.

    Args:
        suffix (str): File extension for the temp file (default: ".txt").
        editor (str | None): Costume editor to use, If None, auto-detect.

    Returns:
        str: Path to the temporary file that the user edited.
    """
    path = _create_temp_file(suffix)

    # Determine editor
    if not editor:
        # Fallback per os
        editor = os.getenv("EDITOR")
        if not editor:
            if sys.platform.startswith("win"):
                editor = "notepad"
            else:
                editor = "nano"

    subprocess.call([editor, path])

    return path

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