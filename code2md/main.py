import argparse
from pathlib import Path

from code2md.clipboard_helper import copy_file_to_clipboard
from code2md.consts import (
    FRONTEND_DEFAULT_EXCLUDED_DIRS,
    FRONTEND_DEFAULT_EXCLUDED_EXTENSIONS,
    FRONTEND_DEFAULT_EXCLUDED_FILES,
    GENERAL_EXCLUDED_DIRS,
    GENERAL_EXCLUDED_FILES,
    PYTHON_DEFAULT_EXCLUDED_DIRS,
    PYTHON_DEFAULT_EXCLUDED_EXTENSIONS,
    PYTHON_DEFAULT_EXCLUDED_FILES,
)
from code2md.file_collector import DefaultFileCollector
from code2md.file_writer import MarkdownFileWriter


def main() -> None:
    """Entry point for the code2md CLI."""
    parser = argparse.ArgumentParser(
        description='Generate a Markdown snapshot of a project: directory tree and file contents.',
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Core arguments
    parser.add_argument(
        'project_path',
        nargs='?',
        default='.',
        help='Path to the project root (default: current directory).',
    )
    parser.add_argument(
        '-o',
        '--output-dir',
        help='Directory where the resulting Markdown file will be saved (default: project directory).',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Enable verbose logging.',
    )

    # Custom exclusions
    parser.add_argument(
        '-d',
        '--exclude-dirs',
        help='Comma-separated list of directory names to exclude (e.g. "dir1,dir2").',
    )
    parser.add_argument(
        '-f',
        '--exclude-files',
        help='Comma-separated list of filenames to exclude (e.g. "file1.txt,file2.json").',
    )
    parser.add_argument(
        '-e',
        '--exclude-extensions',
        help='Comma-separated list of file extensions to exclude (e.g. ".log,.tmp").',
    )

    # Built-in behavior flags
    parser.add_argument(
        '--no-exclude-dotfiles',
        action='store_false',
        dest='exclude_dotfiles',
        help='Include files and directories starting with a dot (by default they are excluded).',
    )
    parser.add_argument(
        '--add-python-defaults',
        action='store_true',
        help='Add standard exclusions for Python projects.',
    )
    parser.add_argument(
        '--add-frontend-defaults',
        action='store_true',
        help='Add standard exclusions for frontend projects.',
    )

    # Clipboard integration
    parser.add_argument(
        '--copy',
        action='store_true',
        help='Copy the generated Markdown file to the system clipboard.',
    )

    parser.set_defaults(exclude_dotfiles=True)
    args = parser.parse_args()

    start_path = Path(args.project_path).resolve()

    # Build exclusion sets
    excluded_dirs = set(GENERAL_EXCLUDED_DIRS)
    excluded_files = set(GENERAL_EXCLUDED_FILES)
    excluded_extensions: set[str] = set()

    if args.add_python_defaults:
        excluded_dirs.update(PYTHON_DEFAULT_EXCLUDED_DIRS)
        excluded_files.update(PYTHON_DEFAULT_EXCLUDED_FILES)
        excluded_extensions.update(PYTHON_DEFAULT_EXCLUDED_EXTENSIONS)

    if args.add_frontend_defaults:
        excluded_dirs.update(FRONTEND_DEFAULT_EXCLUDED_DIRS)
        excluded_files.update(FRONTEND_DEFAULT_EXCLUDED_FILES)
        excluded_extensions.update(FRONTEND_DEFAULT_EXCLUDED_EXTENSIONS)

    if args.exclude_dirs:
        excluded_dirs.update(d.strip() for d in args.exclude_dirs.split(',') if d.strip())

    if args.exclude_files:
        excluded_files.update(f.strip() for f in args.exclude_files.split(',') if f.strip())

    if args.exclude_extensions:
        excluded_extensions.update(f'.{e.strip().lstrip(".")}' for e in args.exclude_extensions.split(',') if e.strip())

    # Resolve output path
    output_dir = Path(args.output_dir).resolve() if args.output_dir else start_path
    output_dir.mkdir(parents=True, exist_ok=True)

    output_filename = f'{start_path.name}_structure.md'
    output_file = output_dir / output_filename

    # Prevent generated file from being included in itself
    excluded_files.add(output_filename)

    # Collect project data
    file_collector = DefaultFileCollector(verbose=args.verbose)
    project_tree, files_to_include = file_collector.collect(
        start_path=start_path,
        excluded_dirs=excluded_dirs,
        excluded_files=excluded_files,
        excluded_extensions=excluded_extensions,
        exclude_dotfiles=args.exclude_dotfiles,
    )

    # Write result
    file_writer = MarkdownFileWriter()
    file_writer.write(output_file, project_tree, files_to_include, start_path)

    # Optional: copy generated file to OS clipboard
    if args.copy:
        try:
            copy_file_to_clipboard(output_file)
            print('📋 Generated Markdown file has been copied to the system clipboard.')
        except Exception as exc:  # noqa: BLE001
            print(f'⚠️ Failed to copy generated file to clipboard: {exc}')

    print(f'✅ Done! Project structure saved to: {output_file}')
    print(f'📊 Total files processed: {len(files_to_include)}')


if __name__ == '__main__':
    main()
