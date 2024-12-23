import os


def parse_tree(tree):
    """
    Parse a text-based directory tree into a nested dictionary.
    """
    lines = tree.strip().split("\n")
    structure = {}
    stack = []
    current_dict = structure

    for line in lines:
        indent_level = len(line) - len(line.lstrip(" "))
        name = line.strip(" ├──│└─")

        while len(stack) > indent_level:
            stack.pop()
            current_dict = stack[-1] if stack else structure

        if line.endswith("/"):
            current_dict[name] = {}
            stack.append(current_dict[name])
            current_dict = current_dict[name]
        else:
            current_dict[name] = None

    return structure


def create_structure(base_path, structure):
    """
    Recursively create directories and files based on the parsed structure.
    """
    for name, content in structure.items():
        current_path = os.path.join(base_path, name)
        if content is None:
            open(current_path, "a").close()
        else:
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
