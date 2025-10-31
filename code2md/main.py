import argparse
from pathlib import Path

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


def main():
    """Основная функция для запуска утилиты из командной строки."""
    parser = argparse.ArgumentParser(
        description='Собирает структуру проекта и содержимое файлов в один Markdown-файл.',
        formatter_class=argparse.RawTextHelpFormatter
    )

    # --- Основные аргументы ---
    parser.add_argument(
        'project_path', nargs='?', default='.',
        help='Путь к директории проекта (по умолчанию: текущая директория).'
    )
    parser.add_argument(
        '-o', '--output-dir',
        help='Папка для сохранения итогового файла (по умолчанию: папка проекта).'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Включить подробный вывод процесса работы.'
    )

    # --- Аргументы для кастомных исключений ---
    parser.add_argument(
        '-d', '--exclude-dirs',
        help='Директории для исключения, через запятую (например: "dir1,dir2").'
    )
    parser.add_argument(
        '-f', '--exclude-files',
        help='Файлы для исключения, через запятую (например: "file1.txt,file2.json").'
    )
    parser.add_argument(
        '-e', '--exclude-extensions',
        help='Расширения файлов для исключения, через запятую (например: ".log,.tmp").'
    )

    # --- Аргументы для управления поведением по умолчанию ---
    parser.add_argument(
        '--no-exclude-dotfiles', action='store_false', dest='exclude_dotfiles',
        help='Включает в отчет файлы и папки, начинающиеся с точки (по умолчанию исключены).'
    )
    parser.add_argument(
        '--add-python-defaults', action='store_true',
        help='Добавить стандартные исключения для Python-проектов.'
    )
    parser.add_argument(
        '--add-frontend-defaults', action='store_true',
        help='Добавить стандартные исключения для Frontend-проектов.'
    )
    parser.set_defaults(exclude_dotfiles=True)

    args = parser.parse_args()

    start_path = Path(args.project_path).resolve()

    # --- Формирование списков исключений ---
    excluded_dirs = set(GENERAL_EXCLUDED_DIRS)
    excluded_files = set(GENERAL_EXCLUDED_FILES)
    excluded_extensions = set()

    # Добавляем стандартные наборы, если указаны флаги
    if args.add_python_defaults:
        excluded_dirs.update(PYTHON_DEFAULT_EXCLUDED_DIRS)
        excluded_files.update(PYTHON_DEFAULT_EXCLUDED_FILES)
        excluded_extensions.update(PYTHON_DEFAULT_EXCLUDED_EXTENSIONS)

    if args.add_frontend_defaults:
        excluded_dirs.update(FRONTEND_DEFAULT_EXCLUDED_DIRS)
        excluded_files.update(FRONTEND_DEFAULT_EXCLUDED_FILES)
        excluded_extensions.update(FRONTEND_DEFAULT_EXCLUDED_EXTENSIONS)

    # Добавляем кастомные исключения
    if args.exclude_dirs:
        excluded_dirs.update(d.strip() for d in args.exclude_dirs.split(','))
    if args.exclude_files:
        excluded_files.update(f.strip() for f in args.exclude_files.split(','))
    if args.exclude_extensions:
        excluded_extensions.update(f'.{e.strip().lstrip(".")}' for e in args.exclude_extensions.split(','))

    # --- Определение выходного файла ---
    output_dir = Path(args.output_dir) if args.output_dir else start_path
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f'project_{start_path.name}_structure.md'

    # --- Сбор и запись ---
    file_collector = DefaultFileCollector(verbose=args.verbose)
    project_tree, files_to_include = file_collector.collect(
        start_path,
        excluded_dirs,
        excluded_files,
        excluded_extensions,
        args.exclude_dotfiles
    )

    file_writer = MarkdownFileWriter()
    file_writer.write(output_file, project_tree, files_to_include, start_path)

    print(f'✅ Готово! Структура проекта сохранена в файл: {output_file}')
    print(f'📊 Всего файлов обработано: {len(files_to_include)}')


if __name__ == '__main__':
    main()
