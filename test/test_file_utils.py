"""
Unit test for src.anmu_buddy.file_utils

This test suite covers create_temp_file and delete_file functions.

Key aspects tested:
- File creation with default and custom suffixes
- File writability and existence
- Handling of invalid suffixes (ValueError)
- Normal deletion of temporary files
- Blocking deletion of files outside the temp directory
- Behavior when file does not exist
- Handling OSError during deletion
- Ensuring proper cleanup of temporary files after tests
"""

import os
import logging

import pytest
from src.anmu_buddy.file_utils import create_temp_file, delete_file


def test_create_temp_file_default_suffix_and_exist():
    """Verify that create_temp_file creates an absolute path, file exists,
    and the temporary file is cleaned up after the test.
    """
    path = create_temp_file()
    try:
        assert os.path.isabs(path), "Path must be absolute"
        assert os.path.exists(path), "File must exist after creation"
        assert path.endswith(".txt"), "Default suffix must be '.txt'"
    finally:
        delete_file(path)
        assert not os.path.exists(path), "File must be deleted after cleanup"


def test_create_temp_file_custom_suffix_and_writable():
    """Verify create_temp_file supports a custom suffix and allows writing/reading data.
    Ensures cleanup of the temporary file after test completion.
    """
    suffix = ".log"
    path = create_temp_file(suffix=suffix)
    try:
        assert path.endswith(suffix), "Custom suffix is applied"

        test_content = "sample text"
        with open(path, "w", encoding="utf-8") as f:
            f.write(test_content)
        with open(path, "r", encoding="utf-8") as f:
            assert f.read() == test_content
    finally:
        delete_file(path)
        assert not os.path.exists(path), "Temporary file should be deleted"


@pytest.mark.parametrize("bad_suffix", ["txt", "a/b.txt", "a\\b.txt"])
def test_create_temp_file_invalid_suffix(bad_suffix):
    """Ensure create_temp_file raises ValueError for invalid suffix inputs."""
    with pytest.raises(ValueError):
        create_temp_file(suffix=bad_suffix)


def test_delete_file_normal(tmp_path):
    """Test that delete_file correctly removes a file in the system temp directory."""
    temp_file = tmp_path / "testfile.txt"
    temp_file.write_text("hello")  # Fixed typo: write_txt -> write_text

    system_temp_file = os.path.join(tmp_path.gettempdir(), temp_file.name)
    os.rename(temp_file, system_temp_file)

    delete_file(system_temp_file)
    assert not os.path.exists(system_temp_file)


def test_delete_file_blocks_non_temp_file(tmp_path, caplog):
    """Verify delete_file does not remove files outside the system temp directory and logs a warning."""
    file_path = tmp_path / "outside_temp.txt"
    file_path.write_text("hello")

    with caplog.at_level(logging.WARNING):
        delete_file(str(file_path))
        assert os.path.exists(file_path)
        assert any("Deletion blocked for non-temporary file" in msg for msg in caplog.messages)


def test_delete_file_no_error_if_not_exist(tmp_path):
    """Ensure delete_file does not raise an error if the target file does not exist."""
    non_exist_path = tmp_path / "non_existing_file.txt"

    if non_exist_path.exists():
        non_exist_path.unlink()
    
    delete_file(str(non_exist_path))
    assert not non_exist_path.exists(), "delete_file() must not create any file"


def test_delete_file_handles_oserror(monkeypatch, tmp_path, caplog):
    """Test that delete_file logs a warning instead of raising when os.remove raises OSError."""
    temp_file = tmp_path / "tempfile.txt"
    temp_file.write_text("hello")
    system_temp_file = os.path.join(tmp_path.gettempdir(), temp_file.name)
    os.rename(temp_file, system_temp_file)

    # Simulate OSError on os.remove
    def fake_remove(path):
        raise OSError("forced error")
    monkeypatch.setattr("os.remove", fake_remove)  # Fixed typo: setsttr -> setattr

    with caplog.at_level(logging.WARNING):
        delete_file(system_temp_file)
        assert any("Failed to delete" in msg for msg in caplog.messages)