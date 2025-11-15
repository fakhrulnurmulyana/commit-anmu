import subprocess
from pathlib import Path
from typing import Union, List

from .input_helper import ask_until_valid
from .validator import (
    is_valid_email,
    is_valid_remote_url,
    is_valid_username,
)

class GitAutomation:
    """
    Utility class to automate basic Git operations such as add, commit, and push.

    This class assumes that Git is installed and the provided repository path
    is a valid Git repository.
    """

    def __init__(self, repo_path=None):
        """
        Initialize the GitAutomation instance.

        Args:
            repo_path (str | Path): Path to the Git repository.

        Raises:
            FileNotFoundError: If the provided path is not a Git repository.
        """
        # Normalize input path
        if repo_path is None:
            # Use current working directory
            self.repo_path = Path.cwd().resolve()
        else:
            self.repo_path = Path(repo_path).resolve()

        # Ensure repo_path is a valid Git repository
        if not (self.repo_path / ".git").exists():
            raise FileNotFoundError(f"The path {self.repo_path} is not a git repository.")
        
        # Get the current active branch (fallback to 'main' if none found)
        self.current_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=self.repo_path, 
            capture_output=True, 
            text=True,
        ).stdout.strip() or "main"
        
    def _run(self, command):
        """
        Execute a Git command using subprocess and handle errors gracefully.

        Args:
            command (list[str]): The Git command and its arguments to run.

        Returns:
            subprocess.CompletedProcess: Result of the executed command.

        Raises:
            RuntimeError: If Git is not installed or the command fails.
        """
        try:
            result = subprocess.run(
                            command,
                            cwd=self.repo_path,
                            capture_output=True,
                            text=True,
                            check=True,
                        )
            if result.stdout:
                print(result.stdout, end="") # Show Git output if available
            return result
        
        except FileNotFoundError as e:
            # Raised when 'git' binary cannot be found
            raise RuntimeError("Git command not found. Make sure Git is installed.") from e
        
        except subprocess.CalledProcessError as e:
            # Raised when Git command returns a non-zero exit status
            error_msg = e.stderr.strip() if e.stderr else "Unknown error"
            raise RuntimeError(
                f"Git command failed: {' '.join(command)}\nError: {error_msg}"
            ) from e
        
    def _add(self, files: Union[str, List[str], tuple[str, ...]])-> None:
        """
        Stage files for commit.

        Args:
            files (str | list[str] | tuple[str, ...]): One or more file paths to add.
        """
        if isinstance(files, (list, tuple)):
            cmd = ["git", "add"] + list(map(str, files))
        else:
            cmd = ["git", "add", str(files)]
        print(f"Staging files: {files}\nBranch (current branch): {self.current_branch}")
        self._run(cmd)

    def _commit(self, message_file: str)-> None:
        """
        Commit staged changes using a message file.

        Args:
            message_file (str): Path to a text file containing the commit message.

        Raises:
            FileNotFoundError: If the message file does not exist.
        """
        message_path = Path(message_file)
        if not message_path.exists():
            raise FileNotFoundError(f"Commit message file not found: {message_path}")
        
        print(f"Committing changes using message from: {message_file}")
        self._run(["git", "commit", "-F", message_path.as_posix()])

    def _validate_git_environment(self) -> dict:
        return {
            "remote": self._run(["git", "remote", "-v"]).stdout.strip(),
            "username": self._run(["git", "config", "user.name"]).stdout.strip(),
            "email": self._run(["git", "config", "user.email"]).stdout.strip(),
        }
    
    def _setup_missing_git_config(self, env: dict) -> None:
        if not env["remote"]:
            remote_url = ask_until_valid(
                "No remote repo found. please input remote URL: ",
                is_valid_remote_url,
                "URL not valid"
            )
            self._run(["git", "remote", "add", "origin", remote_url])
        
        if not env["username"]:
            name = ask_until_valid(
                "Your git username is not set. Input Username: ",
                is_valid_username,
                "Username can't be empty."
            )
            self._run(["git", "config", "--global", "user.name", name])

        if not env["email"]:
            email = ask_until_valid(
                "Your git email is not set. Input email: ",
                is_valid_email,
                "Email format is not valid."
            )
            self._run(["git", "config", "--global", "user.email", email])

    def _push(self, remote: str= "origin", branch: Union[str, None]= None)-> None:
        """
        Push committed changes to a remote branch.

        Args:
            remote (str): Name of the remote repository (default: 'origin').
            branch (str | None): Target branch name (default: current branch).
        """
        if branch is None:
            branch = self.current_branch

        git_env = self._validate_git_environment()
        self._setup_missing_git_config(git_env)
        
        print(f"Pushing changes to {remote}/{branch}")
        self._run(["git", "push", remote, branch])
    
    def commit_change(self, files: Union[str, List[str], tuple[str, ...]], message_file:str)-> None:
        """
        Stage and commit files locally.

        Args:
            files (str | list[str] | tuple[str, ...]): Files to add to staging.
            message_file (str): Commit message file path.
        """
        self._add(files)
        self._commit(message_file)
        print("Changes staged and committed locally")

    def sync_change(
            self, 
            files: Union[str, List[str], tuple[str, ...]], 
            message_file:str, 
            remote:str="origin", 
            branch:str=None,
        )-> None:
        """
        Add, commit, and push changes to the remote repository.

        Args:
            files (str | list[str] | tuple[str, ...]): Files to stage and commit.
            message_file (str): Commit message file path.
            remote (str): Remote name (default: 'origin').
            branch (str | None): Branch name (default: current branch).
        """
        self.commit_change(files, message_file)
        self._push(remote, branch)
        print(f"Changes synced branch {branch} with remote branch successfully")
        return branch