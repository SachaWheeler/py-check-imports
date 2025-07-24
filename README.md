# py-check-imports

A Python CLI tool to scan a Python file or an entire directory for imports that are unnecessary (unused) or duplicated in the code.
Clean up your code by removing unused or duplicate dependencies, making it more readable and efficient.
[See Limitations](#limitations)

Edit: while this works, ruff is a more comprehensive tool that can also check for unused imports, duplicate imports, and many other code quality issues. Consider using [ruff]

## Features

- **Scans single files or directories recursively:** Checks all `.py` files in a directory tree.
- **Detects unused imports:** Highlights unecessary import statements in the file.
- **Detects duplicate imports:** Highlights repeated import statements in the same file.
- **Optional JSON output:** Use `--json` for machine-readable output.
- **CLI tool:** Installable and callable as `py-check-imports`.
- **Reports errors gracefully:** Handles syntax errors, unreadable files, etc.
- **Output is ordered:** Results are sorted by file and line number.

## Installation

You can install locally from the repo:

```bash
pip install .
```

Or use it directly with Python:

```bash
python py_check_imports.py <path>
```

## Usage

### Scan a single file

```bash
py-check-imports myscript.py
```

### Scan a directory recursively

```bash
py-check-imports src/
```

### Output results in JSON

```bash
py-check-imports myscript.py --json
py-check-imports src/ --json
```

### Example output (text)

```
Unused imports found:
src/utils/helpers.py: Line 2: import os
src/utils/helpers.py: Line 5: from math import sqrt

Duplicate imports found:
src/utils/helpers.py: Lines 2, 10: import os

Errors:
src/bad_file.py: SyntaxError: invalid syntax (bad_file.py, line 10)
```

### Example output (JSON)

```json
{
  "unused_imports": [
    {
      "file": "src/utils/helpers.py",
      "line": 2,
      "import_statement": "import os"
    }
  ],
  "duplicate_imports": [
    {
      "file": "src/utils/helpers.py",
      "lines": [2, 10],
      "import_statement": "import os"
    }
  ],
  "errors": [
    {
      "file": "src/bad_file.py",
      "error": "SyntaxError: invalid syntax (bad_file.py, line 10)"
    }
  ]
}
```

## Error Handling

- If a file cannot be read or contains syntax errors, the script will report it and continue analyzing other files.

## Limitations

- This tool analyzes imports using static code analysis (AST). If your code contains dynamic import statements (e.g., using `__import__`, `importlib`, or `eval`/`exec`), or if names are manipulated at runtime, these imports might not be detected or could be reported as unused, even if they are actually used.
- Similarly, wildcard imports (e.g., `from module import *`) may confuse the analysis, and usage of such imports may not be tracked accurately.
- Code that generates or modifies Python source files at runtime is not supported and may produce misleading results.

If your project uses advanced dynamic import techniques, please review the results carefully.

## License

MIT License. See [LICENSE](LICENSE).

## Contributing

Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request.

## Author

Sacha Wheeler
