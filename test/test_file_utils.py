import os
from src.anmu_buddy.file_utils import create_temp_file, delete_file


def test_create_temp_file_default_suffix_and_exist():
    path = create_temp_file()
    try:
        assert os.path.isabs(path), "Path must be absolute"
        assert os.path.exists(path), "File must exist after creation"
        assert path.endswith(".txt"), "Default suffix must be '.txt'"
    finally:
        delete_file(path)
        assert not os.path.exists(path), "File must be deleted after cleanup"

def test_create_temp_file_costume_suffix_and_writable():
    suffix = ".log "
    path = create_temp_file(suffix=suffix)
    try:
        assert path.endswith(suffix), "Costume suffix is applied"

        test_content = "sample text"
        with open(path, "w", encoding="utf-8") as f:
            f.write(test_content)
        with open(path, "r", encoding="utf-8") as f:
            assert f.read() == test_content
    finally:
        delete_file(path)
        assert not os.path.exists(path), "Temporary file should be deleted"

def test_delete_file_no_error_if_not_exist(temp_path):
    non_exist_path = temp_path / "non_existing_file.txt"

    if non_exist_path.exists():
        non_exist_path.unlink()
    
    delete_file(str(non_exist_path))

    assert not non_exist_path.exists(), "delete_file() must not create any file"
