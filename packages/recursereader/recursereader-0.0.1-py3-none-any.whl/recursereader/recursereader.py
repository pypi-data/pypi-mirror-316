import os
import argparse
from pathlib import Path


def load_gitignore_patterns(gitignore_path):
    """
    Load patterns from a .gitignore-like file.

    Parameters:
    - gitignore_path (str): Path to the gitignore file.

    Returns:
    - set: A set of patterns to ignore.
    """
    patterns = set()
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):  # Ignore comments and empty lines
                    patterns.add(line)
    return patterns


def should_ignore(file_path, ignore_patterns):
    """
    Check if a file or directory matches any ignore patterns.

    Parameters:
    - file_path (str): Path to the file or directory.
    - ignore_patterns (set): A set of patterns to check against.

    Returns:
    - bool: True if the file or directory should be ignored, False otherwise.
    """
    for pattern in ignore_patterns:
        if Path(file_path).match(pattern):
            return True
    return False


def print_files_recursively(root_dir, ignore_dot_dirs=True, show_hidden_files=False, max_depth=None,
                            ignore_patterns=set(), ignore_subfolders=[]):
    """
    Recursively print file paths and contents from the given directory.

    Parameters:
    - root_dir (str): The root directory to start the search.
    - ignore_dot_dirs (bool): If True, ignore directories starting with a dot.
    - show_hidden_files (bool): If True, include hidden files in the output.
    - max_depth (int): The maximum depth to traverse.
    - ignore_patterns (set): Patterns to ignore.
    - ignore_subfolders (list): Specific subfolders to ignore.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Apply maximum depth filtering
        if max_depth is not None:
            depth = len(os.path.relpath(dirpath, root_dir).split(os.sep))
            if depth > max_depth:
                continue

        # Ignore dot-directories and specific subfolders
        dirnames[:] = [
            d for d in dirnames
            if not (ignore_dot_dirs and d.startswith("."))
               and not should_ignore(os.path.join(dirpath, d), ignore_patterns)
               and d not in ignore_subfolders
        ]

        # Process each file
        for filename in filenames:
            # Skip hidden files if not requested
            if not show_hidden_files and filename.startswith("."):
                continue

            file_path = os.path.join(dirpath, filename)

            # Skip files matching ignore patterns
            if should_ignore(file_path, ignore_patterns):
                continue

            print(f"Path: {file_path}")
            try:
                # Print file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    print("Contents:")
                    print(file.read())
                    print("-" * 50)  # Separator for readability
            except Exception as e:
                print(f"Could not read file {file_path}. Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Recursively print file paths and contents from a directory."
    )
    parser.add_argument(
        "root_dir",
        type=str,
        help="The root directory to start the search."
    )
    parser.add_argument(
        "--ignore-dot-dirs",
        action="store_true",
        default=True,
        help="Ignore directories starting with a dot (e.g., '.git')."
    )
    parser.add_argument(
        "--show-hidden-files",
        action="store_true",
        default=False,
        help="Include hidden files (files starting with a dot) in the output."
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help="Maximum depth to traverse (e.g., 2 for two levels deep)."
    )
    parser.add_argument(
        "--gitignore",
        type=str,
        default=None,
        help="Path to a .gitignore-like file with patterns to ignore."
    )
    parser.add_argument(
        "--ignore-subfolders",
        nargs="+",
        default=[],
        help="Specific subfolders to ignore (provide a space-separated list)."
    )
    parser.add_argument(
        "--log-to-file",
        type=str,
        default=None,
        help="Specify a file to log the output instead of printing to the console."
    )

    args = parser.parse_args()

    # Load ignore patterns from .gitignore if provided
    ignore_patterns = set()
    if args.gitignore:
        ignore_patterns = load_gitignore_patterns(args.gitignore)

    # Redirect output to a file if specified
    if args.log_to_file:
        with open(args.log_to_file, "w", encoding="utf-8") as log_file:
            with open(os.devnull, "w") as devnull:
                orig_stdout = os.dup(1)  # Duplicate stdout
                os.dup2(log_file.fileno(), 1)  # Redirect stdout to file
                print_files_recursively(
                    root_dir=args.root_dir,
                    ignore_dot_dirs=args.ignore_dot_dirs,
                    show_hidden_files=args.show_hidden_files,
                    max_depth=args.max_depth,
                    ignore_patterns=ignore_patterns,
                    ignore_subfolders=args.ignore_subfolders
                )
                os.dup2(orig_stdout, 1)  # Restore stdout
                os.close(orig_stdout)
    else:
        print_files_recursively(
            root_dir=args.root_dir,
            ignore_dot_dirs=args.ignore_dot_dirs,
            show_hidden_files=args.show_hidden_files,
            max_depth=args.max_depth,
            ignore_patterns=ignore_patterns,
            ignore_subfolders=args.ignore_subfolders
        )


if __name__ == "__main__":
    main()
