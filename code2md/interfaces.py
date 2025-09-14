from abc import ABC, abstractmethod
from pathlib import Path


class FileCollector(ABC):
    """Интерфейс для сбора файлов."""

    @abstractmethod
    def collect(
        self,
        start_path: Path,
        excluded_dirs: set[str],
        excluded_files: set[str],
        excluded_extensions: set[str],
    ) -> tuple[list[str], list[Path]]:
        pass


class FileWriter(ABC):
    """Интерфейс для записи результатов."""

    @abstractmethod
    def write(
        self,
        output_file: Path,
        project_tree: list[str],
        files_to_include: list[Path],
        start_path: Path,
    ) -> None:
        pass
