import logging
import os
from pathlib import Path

from code2md.interfaces import FileCollector


class DefaultFileCollector(FileCollector):
    """Сборщик файлов по умолчанию."""

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        if verbose:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = None

    def collect(
        self,
        start_path: Path,
        excluded_dirs: set[str],
        excluded_files: set[str],
        excluded_extensions: set[str],
        exclude_dotfiles: bool,
    ) -> tuple[list[str], list[Path]]:
        """Собирает структуру директории и список файлов для включения."""
        project_tree = []
        files_to_include = []

        if self.logger:
            self.logger.info(f'Начинаю сбор из: {start_path}')
            self.logger.info(f'Исключенные директории: {excluded_dirs or "Нет"}')
            self.logger.info(f'Исключенные файлы: {excluded_files or "Нет"}')
            self.logger.info(f'Исключенные расширения: {excluded_extensions or "Нет"}')
            self.logger.info(f'Исключать dot-файлы: {"Да" if exclude_dotfiles else "Нет"}')

        for root, dirs, files in os.walk(start_path, topdown=True):
            # Фильтруем директории, чтобы os.walk не заходил в них
            dirs[:] = [
                d
                for d in sorted(dirs)
                if self._should_include(d, excluded_dirs, set(), set(), exclude_dotfiles, is_dir=True)
            ]

            root_path = Path(root)
            level = len(root_path.relative_to(start_path).parts)
            indent = '    ' * level

            if level > 0:
                project_tree.append(f'{indent}📂 {root_path.name}/')

            sub_indent = '    ' * (level + 1)
            for filename in sorted(files):
                if self._should_include(filename, excluded_dirs, excluded_files, excluded_extensions, exclude_dotfiles):
                    file_path = root_path / filename
                    files_to_include.append(file_path)
                    project_tree.append(f'{sub_indent}📄 {filename}')

        return project_tree, files_to_include

    @staticmethod
    def _should_include(
        name: str,
        excluded_dirs: set[str],
        excluded_files: set[str],
        excluded_extensions: set[str],
        exclude_dotfiles: bool,
        is_dir: bool = False,
    ) -> bool:
        """Проверяет, следует ли включить данный файл или директорию."""
        if exclude_dotfiles and name.startswith('.'):
            return False

        if is_dir:
            return name not in excluded_dirs

        if name in excluded_files:
            return False

        return Path(name).suffix.lower() not in excluded_extensions
