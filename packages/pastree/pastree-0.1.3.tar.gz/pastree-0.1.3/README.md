
# pastree 🥐 ˖ 🌴

**pastree** is a command-line tool for generating directory structures from tree-like input. Just paste your desired structure, and `pastree` creates all the necessary directories and files for you.

---

## Features

- Quickly scaffold complex directory structures.
- Supports a tree-style input format for intuitive use.
- Works cross-platform (Linux, macOS, Windows).

---

## Installation

Install `pastree` using `pip`:

```bash
pip install pastree
```

---

## Usage

After installation, run the `pastree` command:

```bash
pastree
```

### Example

1. Run the `pastree` command in your terminal.
2. Paste your desired directory structure (in a tree-like format):

    ```bash
    my_project/
    ├── LICENSE
    ├── README.md
    ├── setup.py
    ├── my_project/
    │   ├── __init__.py
    │   └── main.py
    └── tests/
        ├── __init__.py
        └── test_main.py
    ```

3. Press **Ctrl+D** (Linux/macOS), **Ctrl+Z** (Windows) or press enter twice to finish.

4. `pastree` will create the corresponding directories and touch the files

---

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository.
2. Make your changes in a new branch.
3. Submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Feedback and Support

If you encounter any issues or have suggestions for improvement, feel free to open an issue on [GitHub](https://github.com/yourusername/pastree).

Happy pastree making! 🌳 🌲 🌴
