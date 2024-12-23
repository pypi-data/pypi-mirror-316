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


def test_parse_tree_with_comments():
    """Test parsing a tree structure that contains inline comments."""
    tree_input = """
    my-docker-project/
    ├── Dockerfile                # Docker configuration file to build the image
    ├── docker-compose.yml        # Compose file to manage multi-container setup (optional)
    ├── .dockerignore             # Files and directories to ignore when building the Docker image
    ├── app/                      # Application code folder
    │   ├── __init__.py           # Initialization for Python projects (example)
    │   ├── main.py               # Main entry point for the application
    │   └── requirements.txt      # Python dependencies (if using Python)
    ├── config/                   # Configuration files (optional)
    │   └── settings.yaml         # Example configuration file
    ├── tests/                    # Test code for the application
    │   ├── test_main.py          # Example test file
    │   └── __init__.py           # Initialization for Python test package
    ├── logs/                     # Logs directory (optional)
    ├── data/                     # Data directory for databases or other persistent storage (optional)
    ├── scripts/                  # Utility scripts for the project
    │   └── setup.sh              # Example setup script
    ├── README.md                 # Project documentation
    ├── .env                      # Environment variables file
    └── LICENSE                   # License file for your project (optional)
    """
    expected = {
        "my-docker-project": {
            "Dockerfile": None,
            "docker-compose.yml": None,
            ".dockerignore": None,
            "app": {"__init__.py": None, "main.py": None, "requirements.txt": None},
            "config": {"settings.yaml": None},
            "tests": {"test_main.py": None, "__init__.py": None},
            "logs": {},
            "data": {},
            "scripts": {"setup.sh": None},
            "README.md": None,
            ".env": None,
            "LICENSE": None,
        }
    }

    assert parse_tree(tree_input) == expected
