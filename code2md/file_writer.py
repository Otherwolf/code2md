from pathlib import Path

from code2md.consts import LANGUAGE_MAP
from code2md.interfaces import FileWriter


class MarkdownFileWriter(FileWriter):
    """Записывает результаты в формате Markdown."""

    @classmethod
    def _is_binary_file(cls, file_path: Path) -> bool:
        """Проверяет, является ли файл бинарным.

        Args:
            file_path: Путь к файлу

        Returns:
            True, если файл бинарный, иначе False
        """
        try:
            # Читаем первые 1024 байта файла
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)

            # Проверяем наличие нулевых байтов (признак бинарных файлов)
            if b'\x00' in chunk:
                return True

            # Проверяем, можно ли декодировать как текст UTF-8
            chunk.decode('utf-8')
            return False
        except UnicodeDecodeError:
            return True
        except Exception:
            # В случае ошибки считаем файл текстовым
            return False

    @classmethod
    def _get_language_for_file(cls, file_path: Path) -> str:
        """Определяет язык для подсветки синтаксиса на основе расширения файла или имени файла.

        Args:
            file_path: Путь к файлу

        Returns:
            Строка с названием языка для подсветки синтаксиса
        """
        # Проверяем точное совпадение с именем файла (для специальных файлов типа Dockerfile)
        file_name = file_path.name
        if file_name in LANGUAGE_MAP:
            return LANGUAGE_MAP[file_name]

        # Проверяем расширение файла
        extension = file_path.suffix.lower()
        if extension in LANGUAGE_MAP:
            return LANGUAGE_MAP[extension]

        # Для файлов без расширения или с неизвестным расширением возвращаем пустую строку
        return ''

    @classmethod
    def write(
        self,
        output_file: Path,
        project_tree: list[str],
        files_to_include: list[Path],
        start_path: Path,
    ) -> None:
        """Записывает структуру проекта и содержимое файлов в Markdown файл.

        Args:
            output_file: Путь к выходному файлу
            project_tree: Список строк дерева проекта
            files_to_include: Список путей к файлам для включения
            start_path: Путь к корневой директории проекта
        """
        with output_file.open('w', encoding='utf-8') as f:
            # Часть 1: Структура проекта
            f.write(f'# 🌳 Структура проекта: {start_path.name}\n\n')
            f.write('```\n')
            f.write('\n'.join(project_tree))
            f.write('\n```\n\n')
            f.write('---\n\n')

            # Часть 2: Содержимое файлов
            f.write('# 📜 Содержимое файлов\n\n')

            for file_path in files_to_include:
                relative_path = file_path.relative_to(start_path)
                language = self._get_language_for_file(file_path)

                f.write(f'## 📄 Файл: `{relative_path}`\n')

                # Если файл бинарный, не пытаемся его читать
                if self._is_binary_file(file_path):
                    f.write('```text\n')
                    f.write('[Бинарный файл - содержимое не отображается]\n')
                    f.write('```\n\n')
                    continue

                # Добавляем подсветку синтаксиса, если язык определен
                if language:
                    f.write(f'```{language}\n')
                else:
                    f.write('```\n')

                try:
                    content = file_path.read_text(encoding='utf-8')
                    # Убираем только завершающие пробелы и пустые строки в конце
                    f.write(content.rstrip())
                except UnicodeDecodeError:
                    f.write('[Файл содержит не-UTF-8 символы - содержимое не отображается]')
                except Exception as e:
                    f.write(f'Не удалось прочитать файл: {e!s}')
                f.write('\n```\n\n')
