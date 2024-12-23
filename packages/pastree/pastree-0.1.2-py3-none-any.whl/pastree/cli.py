import os


def parse_tree(tree):
    """
    Parse a text-based directory tree into a nested dictionary.
    """
    lines = tree.strip().split("\n")
    structure = {}
    stack = [(0, structure)]  # Tracks (indent_level, current_dict)

    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        # Count the actual spaces before any tree characters
        stripped_line = line.replace("│", " ")  # Replace vertical line with space
        indent_spaces = len(stripped_line) - len(stripped_line.lstrip())
        indent_level = indent_spaces // 2  # Tree characters use 2-space indentation

        # Clean the name
        name = line.strip()
        for char in ["├── ", "└── ", "│   ", "    ", "/"]:
            name = name.replace(char, "")
        name = name.strip()

        # Pop from stack until we find the parent level, but keep at least the root
        while len(stack) > 1 and stack[-1][0] >= indent_level:
            stack.pop()

        # Get current dictionary from the last item in stack
        current_dict = stack[-1][1]

        # Add to structure
        if line.strip().endswith("/"):  # Directory
            current_dict[name] = {}
            stack.append((indent_level, current_dict[name]))
        else:  # File
            current_dict[name] = None

    return structure


def create_structure(base_path, structure):
    """
    Recursively create directories and files based on the parsed structure.
    """
    for name, content in structure.items():
        current_path = os.path.join(base_path, name)
        if content is None:  # It's a file
            os.makedirs(os.path.dirname(current_path), exist_ok=True)
            open(current_path, "a").close()
        else:  # It's a directory
            os.makedirs(current_path, exist_ok=True)
            create_structure(current_path, content)


def main():
    print(
        "Paste your directory tree structure below, then press Enter and Ctrl+D (Linux/Mac) or Enter and Ctrl+Z (Windows):"
    )
    try:
        tree_input = "\n".join(iter(input, ""))
    except EOFError:
        pass

    if not tree_input.strip():
        print("No input provided. Exiting.")
        return

    parsed_structure = parse_tree(tree_input)
    create_structure(".", parsed_structure)
    print("Directory structure created!")


if __name__ == "__main__":
    main()
