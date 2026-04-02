from pathlib import Path

from code2md.consts import LANGUAGE_MAP
from code2md.interfaces import FileWriter


class MarkdownFileWriter(FileWriter):
    """Записывает результаты в формате Markdown."""

    _TEXT_BYTES = bytes(range(32, 127)) + b'\n\r\t\f\b'
    _CHUNK_SIZE = 8192
    _BINARY_THRESHOLD = 0.30

    @classmethod
    def _is_binary_file(cls, file_path: Path) -> bool:
        """Проверяет, является ли файл бинарным.

        Args:
            file_path: Путь к файлу

        Returns:
            True, если файл бинарный, иначе False
        """
        try:
            with file_path.open('rb') as f:
                chunk = f.read(cls._CHUNK_SIZE)

            if not chunk:
                return False

            if b'\x00' in chunk:
                return True

            try:
                chunk.decode('utf-8')
                return False
            except UnicodeDecodeError as exc:
                if exc.start >= len(chunk) - 4:
                    try:
                        chunk.decode('utf-8', errors='ignore')
                        return False
                    except Exception:
                        pass

            nontext = sum(byte not in cls._TEXT_BYTES for byte in chunk)
            return (nontext / len(chunk)) > cls._BINARY_THRESHOLD

        except OSError:
            return False

    @classmethod
    def _get_language_for_file(cls, file_path: Path) -> str:
        """Определяет язык для подсветки синтаксиса на основе расширения файла или имени файла.

        Args:
            file_path: Путь к файлу

        Returns:
            Строка с названием языка для подсветки синтаксиса
        """
        file_name = file_path.name
        if file_name in LANGUAGE_MAP:
            return LANGUAGE_MAP[file_name]

        extension = file_path.suffix.lower()
        if extension in LANGUAGE_MAP:
            return LANGUAGE_MAP[extension]

        return ''

    @classmethod
    def write(
        cls,
        output_file: Path,
        project_tree: list[str],
        files_to_include: list[Path],
        start_path: Path,
        use_markers: bool = False,
    ) -> None:
        """Записывает структуру проекта и содержимое файлов в Markdown файл.

        Args:
            output_file: Путь к выходному файлу
            project_tree: Список строк дерева проекта
            files_to_include: Список путей к файлам для включения
            start_path: Путь к корневой директории проекта
            use_markers: Добавлять ли явные маркеры начала/конца файла
        """
        with output_file.open('w', encoding='utf-8') as f:
            f.write(f'# 🌳 Структура проекта: {start_path.name}\n\n')
            f.write('```\n')
            f.write('\n'.join(project_tree))
            f.write('\n```\n\n')
            f.write('---\n\n')

            f.write('# 📜 Содержимое файлов\n\n')

            for file_path in files_to_include:
                relative_path = file_path.relative_to(start_path)
                language = cls._get_language_for_file(file_path)

                if use_markers:
                    f.write(f'<!-- FILE: {relative_path} START -->\n')

                f.write(f'### 📄 Файл: `{relative_path}`\n')

                if cls._is_binary_file(file_path):
                    f.write('[Бинарный файл - содержимое не отображается]\n')

                    if use_markers:
                        f.write(f'<!-- FILE: {relative_path} END -->\n')

                    f.write('\n')
                    continue

                try:
                    content = file_path.read_text(encoding='utf-8')
                except UnicodeDecodeError:
                    f.write('[Файл содержит не-UTF-8 символы - содержимое не отображается]\n')

                    if use_markers:
                        f.write(f'<!-- FILE: {relative_path} END -->\n')

                    f.write('\n')
                    continue
                except Exception as e:
                    f.write(f'Не удалось прочитать файл: {e!s}\n')

                    if use_markers:
                        f.write(f'<!-- FILE: {relative_path} END -->\n')

                    f.write('\n')
                    continue

                if not content.strip():
                    f.write('[Пустой файл]\n')

                    if use_markers:
                        f.write(f'<!-- FILE: {relative_path} END -->\n')

                    f.write('\n')
                    continue

                if language:
                    f.write(f'```{language}\n')
                else:
                    f.write('```\n')

                f.write(content.rstrip())
                f.write('\n```\n')

                if use_markers:
                    f.write(f'<!-- FILE: {relative_path} END -->\n')

                f.write('\n')
