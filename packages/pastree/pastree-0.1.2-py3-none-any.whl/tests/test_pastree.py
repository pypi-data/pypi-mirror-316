import os
import shutil
import pytest
from pastree.cli import parse_tree, create_structure


@pytest.fixture
def cleanup():
    """Cleanup the test directory after each test."""
    yield
    if os.path.exists("test_output"):
        shutil.rmtree("test_output")


def test_parse_empty_tree():
    """Test parsing an empty tree."""
    assert parse_tree("") == {}
    assert parse_tree("\n") == {}
    assert parse_tree("    \n   \n") == {}


def test_parse_single_level():
    """Test parsing a single-level tree with no nesting."""
    tree_input = """
    project/
    ├── file1.txt
    ├── file2.py
    └── file3.md
    """
    expected = {
        "project": {
            "file1.txt": None,
            "file2.py": None,
            "file3.md": None,
        }
    }
    assert parse_tree(tree_input) == expected


def test_parse_deep_nesting():
    """Test parsing deeply nested directories."""
    tree_input = """
    project/
    └── level1/
        └── level2/
            └── level3/
                └── file.txt
    """
    expected = {"project": {"level1": {"level2": {"level3": {"file.txt": None}}}}}
    assert parse_tree(tree_input) == expected


def test_parse_mixed_structure():
    """Test parsing a mixed structure with files and directories at different levels."""
    tree_input = """
    project/
    ├── main.py
    ├── utils/
    │   ├── helpers.py
    │   └── validators/
    │       └── rules.py
    └── tests/
        ├── test_main.py
        └── test_helpers.py
    """
    expected = {
        "project": {
            "main.py": None,
            "utils": {
                "helpers.py": None,
                "validators": {
                    "rules.py": None,
                },
            },
            "tests": {
                "test_main.py": None,
                "test_helpers.py": None,
            },
        }
    }
    assert parse_tree(tree_input) == expected


def test_parse_non_ascii_characters():
    """Test parsing tree with non-ASCII characters in filenames."""
    tree_input = """
    项目/
    ├── 文件1.txt
    └── 文件夹/
        └── 文件2.txt
    """
    expected = {"项目": {"文件1.txt": None, "文件夹": {"文件2.txt": None}}}
    assert parse_tree(tree_input) == expected


def test_create_structure_empty(cleanup):
    """Test creating an empty structure."""
    create_structure("test_output", {})
    assert os.path.exists("test_output") == False


def test_create_structure_single_level(cleanup):
    """Test creating a single-level structure."""
    structure = {"project": {"file1.txt": None, "file2.py": None}}
    create_structure("test_output", structure)

    assert os.path.exists("test_output/project")
    assert os.path.exists("test_output/project/file1.txt")
    assert os.path.exists("test_output/project/file2.py")


def test_create_structure_nested(cleanup):
    """Test creating a nested directory structure."""
    structure = {
        "project": {
            "src": {"main.py": None, "utils": {"helpers.py": None}},
            "tests": {"test_main.py": None},
        }
    }
    create_structure("test_output", structure)

    assert os.path.exists("test_output/project/src/main.py")
    assert os.path.exists("test_output/project/src/utils/helpers.py")
    assert os.path.exists("test_output/project/tests/test_main.py")


def test_create_structure_with_empty_dirs(cleanup):
    """Test creating a structure with empty directories."""
    structure = {"project": {"empty_dir": {}, "nested": {"also_empty": {}}}}
    create_structure("test_output", structure)

    assert os.path.exists("test_output/project/empty_dir")
    assert os.path.exists("test_output/project/nested/also_empty")


def test_edge_cases():
    """Test various edge cases in tree parsing."""
    # Test multiple consecutive empty lines
    assert parse_tree("\n\n\n") == {}

    # Test spaces only
    assert parse_tree("   \n   \n   ") == {}

    # Test single file with no directory
    assert parse_tree("file.txt") == {"file.txt": None}

    # Test directory with trailing slash variations
    assert parse_tree("dir/") == {"dir": {}}
    assert parse_tree("dir////") == {"dir": {}}
