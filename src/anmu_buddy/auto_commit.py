import subprocess
import tempfile
import os

def main():
    """
    Launches Notepad fro writing a git commit message, commits all staged changes,
    and removes the temporary file afterward.

    This function performs the following steps:
        1. Creates a temporary text file for the commit message.
        2. Opens the file in Notepad for the user to write the message.
        3. Executes 'git add .' to stage all changes in the repository.
        4. Execute 'git commit -F <tempfile>' to commit with the message from the file.
        5. Deletes the temporary file after committing.

    Raises:
        FileNotfoundError: If Notepad or Git is not available in the system PATH.
        subprocess.CalledProcessError: If any Git command fails during execution
    """
    # Create temporary file to store commit message.
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        msg_path = tmp.name
    
    current_branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()

    # Open Notepad for the user to write a commit message.
    # The script will pause until the user closes repository.
    subprocess.run(["notepad", msg_path])

    try:
        subprocess.run(["git", "add", "."], check=True) # Stage all changes in the current repository.
        subprocess.run(["git", "commit", "-F", msg_path], check=True) # commit using the message stored in the temporary file.
        subprocess.run(["git", "push", "origin", current_branch], check=True) # push commit
    finally:
        # Clean up the temporary file to avoid leaving unnecessary file behind.
        os.remove(msg_path)

if __name__ == "__main__":
    main()