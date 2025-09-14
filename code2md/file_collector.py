import logging
import os
from pathlib import Path

from code2md.interfaces import FileCollector


class DefaultFileCollector(FileCollector):
    """Сборщик файлов по умолчанию."""

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        if verbose:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = None

    def collect(
            self,
            start_path: Path,
            excluded_dirs: set[str],
            excluded_files: set[str],
            excluded_extensions: set[str],
    ) -> tuple[list[str], list[Path]]:
        """Собирает структуру директории и список файлов для включения.

        Args:
            start_path: Путь к корневой директории для сканирования
            excluded_dirs: Множество папок для исключения
            excluded_files: Множество файлов для исключения
            excluded_extensions: Множество расширений для исключения

        Returns:
            Кортеж из (дерево проекта, список файлов для включения)
        """
        project_tree = []
        files_to_include = []

        if self.logger:
            self.logger.info(f'Start collecting files from the directory: {start_path}')
            self.logger.info(f'Excluded directories: {excluded_dirs}')
            self.logger.info(f'Excluded files: {excluded_files}')
            self.logger.info(f'Excluded extensions: {excluded_extensions}')

        # Используем os.walk для рекурсивного обхода
        for root, dirs, files in os.walk(start_path, topdown=True):
            # Исключаем ненужные директории из дальнейшего обхода
            dirs[:] = [d for d in sorted(dirs) if self._should_include_dir(d, excluded_dirs)]

            root_path = Path(root)
            level = len(root_path.relative_to(start_path).parts)
            indent = '    ' * level

            # Добавляем текущую папку в дерево
            dir_name = root_path.name if level > 0 else start_path.name
            project_tree.append(f'{indent}📂 {dir_name}/')

            if self.logger:
                self.logger.info(f'Processing the directory: {root_path}')

            sub_indent = '    ' * (level + 1)
            processed_files = 0

            for filename in sorted(files):
                if self._should_include_file(filename, excluded_files, excluded_extensions):
                    file_path = root_path / filename
                    files_to_include.append(file_path)
                    project_tree.append(f'{sub_indent}📄 {filename}')
                    processed_files += 1

            if self.logger and processed_files > 0:
                self.logger.info(f'  Added files: {processed_files}')

        if self.logger:
            self.logger.info(f'Total files to include: {len(files_to_include)}')

        return project_tree, files_to_include

    @staticmethod
    def _should_include_dir(dir_name: str, excluded_dirs: set[str]) -> bool:
        """Проверяет, следует ли включить директорию."""
        return dir_name not in excluded_dirs and not any(
            ex_dir in dir_name for ex_dir in excluded_dirs if 'egg-info' in ex_dir)

    @staticmethod
    def _should_include_file(filename: str, excluded_files: set[str], excluded_extensions: set[str]) -> bool:
        """Проверяет, следует ли включить файл."""
        return filename not in excluded_files and Path(filename).suffix not in excluded_extensions
