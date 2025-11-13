import pytest
import subprocess
from unittest.mock import patch, MagicMock
from src.anmu_buddy.git_utils import GitAutomation


@pytest.fixture
def mock_repo(tmp_path):
    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    (repo_path / ".git").mkdir()
    return repo_path


@patch("subprocess.run")
def test_init_with_valid_repo(mock_run, mock_repo):
    mock_run.return_value = MagicMock(stdout="main\n")
    git = GitAutomation(mock_repo)
    assert git.repo_path == mock_repo.resolve()
    assert git.current_branch == "main"
    mock_run.assert_called_once()


def test_init_with_invalid_repo(tmp_path):
    with pytest.raises(FileNotFoundError):
        GitAutomation(tmp_path)


@patch("subprocess.run")
def test_run_success(mock_run, mock_repo):
    mock_run.return_value = MagicMock(stdout="success\n", returncode=0)
    git = GitAutomation(mock_repo)
    result = git._run(["git", "status"])
    assert result.stdout.strip() == "success"
    mock_run.assert_called_with(
        ["git", "status"],
        cwd=mock_repo,
        capture_output=True,
        text=True,
        check=True,
    )


@patch("src.anmu_buddy.git_utils.subprocess.run", side_effect=FileNotFoundError)
def test_run_git_not_installed(mock_run, mock_repo):
    git = GitAutomation(mock_repo)
    with pytest.raises(RuntimeError, match="Git command not found"):
        git._run(["git", "status"])


@patch("subprocess.run")
def test_run_git_command_fails(mock_run, mock_repo):
    mock_run.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd="git commit", stderr="fatal: error"
    )
    git = GitAutomation(mock_repo)
    with pytest.raises(RuntimeError, match="Git command failed"):
        git._run(["git", "commit"])


@patch.object(GitAutomation, "_run")
def test_add_single_file(mock_run, mock_repo):
    git = GitAutomation(mock_repo)
    git._add("file.txt")
    mock_run.assert_called_once_with(["git", "add", "file.txt"])


@patch.object(GitAutomation, "_run")
def test_add_multiple_files(mock_run, mock_repo):
    git = GitAutomation(mock_repo)
    git._add(["a.txt", "b.txt"])
    mock_run.assert_called_once_with(["git", "add", "a.txt", "b.txt"])


@patch.object(GitAutomation, "_run")
def test_commit_success(mock_run, mock_repo, tmp_path):
    message_file = tmp_path / "msg.txt"
    message_file.write_text("commit message")
    git = GitAutomation(mock_repo)
    git._commit(message_file)
    mock_run.assert_called_once_with(["git", "commit", "-F", message_file.as_posix()])


@patch.object(GitAutomation, "_run")
def test_commit_message_file_not_found(mock_run, mock_repo):
    git = GitAutomation(mock_repo)
    with pytest.raises(FileNotFoundError):
        git._commit("no_file.txt")


@patch.object(GitAutomation, "_run")
def test_push_default_branch(mock_run, mock_repo):
    git = GitAutomation(mock_repo)
    git._push()
    mock_run.assert_called_once_with(["git", "push", "origin", git.current_branch])


@patch.object(GitAutomation, "_run")
def test_push_custom_branch(mock_run, mock_repo):
    git = GitAutomation(mock_repo)
    git._push(remote="upstream", branch="dev")
    mock_run.assert_called_once_with(["git", "push", "upstream", "dev"])


@patch.multiple(GitAutomation, _add=MagicMock(), _commit=MagicMock())
def test_commit_change(mock_repo):
    git = GitAutomation(mock_repo)
    git.commit_change("file.txt", "msg.txt")
    git._add.assert_called_once_with("file.txt")
    git._commit.assert_called_once_with("msg.txt")


@patch.multiple(GitAutomation, _add=MagicMock(), _commit=MagicMock(), _push=MagicMock())
def test_sync_change(mock_repo):
    git = GitAutomation(mock_repo)
    git.sync_change(["file.txt"], "msg.txt")
    git._add.assert_called_once()
    git._commit.assert_called_once()
    git._push.assert_called_once()