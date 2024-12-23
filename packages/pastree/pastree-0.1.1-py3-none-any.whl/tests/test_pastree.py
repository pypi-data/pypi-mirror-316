import os
import shutil
from pastree.cli import parse_tree, create_structure


def test_pastree():
    # Define sample input and expected output
    tree_input = """
    sample_project/
    ├── LICENSE
    ├── README.md
    └── sample_project/
        ├── __init__.py
        └── main.py
    """
    base_path = "test_output"
    parsed_structure = parse_tree(tree_input)

    # Create the structure
    create_structure(base_path, parsed_structure)

    # Check directory and files exist
    assert os.path.exists(os.path.join(base_path, "sample_project/LICENSE"))
    assert os.path.exists(
        os.path.join(base_path, "sample_project/sample_project/__init__.py")
    )
    assert os.path.exists(
        os.path.join(base_path, "sample_project/sample_project/main.py")
    )

    # Clean up
    shutil.rmtree(base_path)
