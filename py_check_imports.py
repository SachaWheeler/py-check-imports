#!/usr/bin/env python3
import ast
import os
import sys
import argparse
import json
from collections import defaultdict
from typing import List, Dict, Set, Tuple


def find_unused_and_duplicate_imports_in_file(
    filename: str,
) -> Tuple[List[Dict], List[Dict]]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=filename)
    except (FileNotFoundError, PermissionError) as e:
        return ([{"file": filename, "error": str(e)}], [])
    except SyntaxError as e:
        return ([{"file": filename, "error": f"SyntaxError: {e}"}], [])

    imports: Set[str] = set()
    import_aliases: Dict[str, Tuple[int, str]] = {}
    import_statements: Dict[str, List[int]] = defaultdict(list)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname if alias.asname else alias.name.split(".")[0]
                stmt_str = f"import {alias.name}" + (
                    f" as {alias.asname}" if alias.asname else ""
                )
                imports.add(name)
                import_aliases[name] = (node.lineno, stmt_str)
                import_statements[stmt_str].append(node.lineno)
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ""
            for alias in node.names:
                name = alias.asname if alias.asname else alias.name
                stmt_str = f"from {module} import {alias.name}" + (
                    f" as {alias.asname}" if alias.asname else ""
                )
                imports.add(name)
                import_aliases[name] = (node.lineno, stmt_str)
                import_statements[stmt_str].append(node.lineno)

    used: Set[str] = set()

    class ImportVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            used.add(node.id)

        def visit_Attribute(self, node):
            self.generic_visit(node)

    ImportVisitor().visit(tree)

    unused_imports = imports - used
    unused_results = []
    for name in unused_imports:
        lineno, stmt = import_aliases[name]
        unused_results.append(
            {"file": filename, "line": lineno, "import_statement": stmt}
        )

    duplicate_results = []
    for stmt, lines in import_statements.items():
        if len(lines) > 1:
            duplicate_results.append(
                {"file": filename, "lines": lines, "import_statement": stmt}
            )

    return unused_results, duplicate_results


def find_python_files_in_directory(directory: str) -> List[str]:
    py_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files


def main():
    parser = argparse.ArgumentParser(
        description="Find unused and duplicate imports in Python scripts or directories."
    )
    parser.add_argument("path", help="Path to Python file or directory")
    parser.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )
    args = parser.parse_args()

    all_unused = []
    all_duplicates = []
    all_errors = []

    if os.path.isdir(args.path):
        files = find_python_files_in_directory(args.path)
        if not files:
            print(f"No Python files found in directory: {args.path}", file=sys.stderr)
            sys.exit(1)
        for file in files:
            unused, duplicates = find_unused_and_duplicate_imports_in_file(file)
            # Partition errors out (they will only be in unused)
            file_errors = [res for res in unused if "error" in res]
            file_unused = [res for res in unused if "import_statement" in res]
            all_unused.extend(file_unused)
            all_duplicates.extend(duplicates)
            all_errors.extend(file_errors)
    elif os.path.isfile(args.path):
        unused, duplicates = find_unused_and_duplicate_imports_in_file(args.path)
        file_errors = [res for res in unused if "error" in res]
        file_unused = [res for res in unused if "import_statement" in res]
        all_unused.extend(file_unused)
        all_duplicates.extend(duplicates)
        all_errors.extend(file_errors)
    else:
        print(
            f"Error: '{args.path}' is not a valid file or directory.", file=sys.stderr
        )
        sys.exit(1)

    unused_sorted = sorted(all_unused, key=lambda r: (r["file"], r["line"]))
    duplicates_sorted = sorted(all_duplicates, key=lambda r: (r["file"], r["lines"]))
    errors_sorted = sorted(all_errors, key=lambda r: r["file"])

    if args.json:
        output = {
            "unused_imports": unused_sorted,
            "duplicate_imports": duplicates_sorted,
            "errors": errors_sorted,
        }
        print(json.dumps(output, indent=2))
    else:
        if unused_sorted:
            print("Unused imports found:")
            for res in unused_sorted:
                print(f"{res['file']}: Line {res['line']}: {res['import_statement']}")
        else:
            print("No unused imports found.")

        if duplicates_sorted:
            print("\nDuplicate imports found:")
            for res in duplicates_sorted:
                line_list = ", ".join(str(l) for l in res["lines"])
                print(f"{res['file']}: Lines {line_list}: {res['import_statement']}")
        else:
            print("\nNo duplicate imports found.")

        if errors_sorted:
            print("\nErrors:")
            for err in errors_sorted:
                print(f"{err['file']}: {err['error']}")


if __name__ == "__main__":
    main()
