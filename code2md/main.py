import argparse
import typing
from pathlib import Path

from code2md.file_collector import DefaultFileCollector
from code2md.file_writer import MarkdownFileWriter

if typing.TYPE_CHECKING:
    from code2md.interfaces import FileCollector, FileWriter


class ProjectStructureCollector:
    """Основной класс для сбора структуры проекта (Принцип единственной ответственности - SRP)."""

    def __init__(self, file_collector: 'FileCollector', file_writer: 'FileWriter') -> None:
        self.file_collector = file_collector
        self.file_writer = file_writer

    def collect_and_save(
            self,
            start_path: Path,
            output_file: Path,
            excluded_dirs: set[str],
            excluded_files: set[str],
            excluded_extensions: set[str],
    ) -> None:
        """Собирает структуру проекта и сохраняет результат.

        Args:
            start_path: Путь к корневой директории проекта
            output_file: Путь к выходному файлу
            excluded_dirs: Множество папок для исключения
            excluded_files: Множество файлов для исключения
            excluded_extensions: Множество расширений для исключения
        """
        project_tree, files_to_include = self.file_collector.collect(
            start_path, excluded_dirs, excluded_files, excluded_extensions
        )

        self.file_writer.write(output_file, project_tree, files_to_include, start_path)

        print(f'✅ Структура и содержимое сохранены в {output_file}')
        print(f'📊 Всего файлов обработано: {len(files_to_include)}')


def parse_comma_separated_args(args_str: str) -> set[str]:
    """Парсит строку с аргументами, разделенными запятыми."""
    if not args_str:
        return set()
    return {item.strip() for item in args_str.split(',') if item.strip()}


def get_default_config() -> tuple[set[str], set[str], set[str]]:
    """Возвращает конфигурацию по умолчанию."""
    excluded_dirs = {
        '.git', '.idea', '.vscode', '__pycache__', 'node_modules',
        'dist', '.env', '.venv', 'certs', 'build', 'egg-info',
        '.ruff_cache', '.pytest_cache'
    }

    excluded_files = {
        'uv.lock', 'package-lock.json', '.DS_Store'
    }

    excluded_extensions = {
        '.tgz', '.mp3', '.lock', '.log', '.DS_Store'
    }

    return excluded_dirs, excluded_files, excluded_extensions


def main() -> None:
    """Основная функция приложения."""
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(
        description='Сбор структуры проекта и содержимого файлов',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  code2md
  code2md --exclude-dirs ".git,.idea,build"
  code2md --exclude-files "README.md,config.ini" --exclude-extensions ".txt,.log"
  code2md --output-dir "docs" # Сохранить в папку docs
  code2md --verbose
        """
    )

    parser.add_argument(
        '-d', '--exclude-dirs',
        help='Исключаемые папки (через запятую): ".git,.idea,node_modules"'
    )

    parser.add_argument(
        '-f', '--exclude-files',
        help='Исключаемые файлы (через запятую): "README.md,config.ini"'
    )

    parser.add_argument(
        '-e', '--exclude-extensions',
        help='Исключаемые расширения (через запятую): ".log,.tmp,.bak"'
    )

    parser.add_argument(
        '-o', '--output-dir',
        help='Папка для сохранения итогового файла (по умолчанию - текущая)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Вывод подробной информации о процессе сбора'
    )

    args = parser.parse_args()

    # Получаем конфигурацию по умолчанию
    excluded_dirs, excluded_files, excluded_extensions = get_default_config()

    # Добавляем пользовательские исключения
    if args.exclude_dirs:
        excluded_dirs.update(parse_comma_separated_args(args.exclude_dirs))

    if args.exclude_files:
        excluded_files.update(parse_comma_separated_args(args.exclude_files))

    if args.exclude_extensions:
        excluded_extensions.update(parse_comma_separated_args(args.exclude_extensions))

    # Создаем экземпляры классов
    file_collector = DefaultFileCollector(verbose=args.verbose)
    file_writer = MarkdownFileWriter()
    collector = ProjectStructureCollector(file_collector, file_writer)

    # Определяем пути
    start_path = Path.cwd()
    print(f'Текущая директория: {start_path}')

    # Имя файла для вывода
    output_filename_str = f'{start_path.name}_structure.md'

    # Определяем путь для сохранения файла
    if args.output_dir:
        output_path = Path(args.output_dir)
        # Если путь относительный, делаем его абсолютным относительно текущей директории
        if not output_path.is_absolute():
            output_path = start_path / output_path

        # Создаем директорию, если она не существует
        output_path.mkdir(parents=True, exist_ok=True)

        final_output_file = output_path / output_filename_str
    else:
        # По умолчанию сохраняем в текущей директории
        final_output_file = start_path / output_filename_str

    # Добавляем имя файла в исключения, чтобы он не попал сам в себя
    excluded_files.add(output_filename_str)

    # Выполняем сбор и сохранение
    collector.collect_and_save(
        start_path,
        final_output_file,
        excluded_dirs,
        excluded_files,
        excluded_extensions
    )


if __name__ == '__main__':
    main()
