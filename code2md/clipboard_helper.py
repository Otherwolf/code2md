from __future__ import annotations

from pathlib import Path
import platform
import subprocess


class ClipboardFileCopyError(RuntimeError):
    """Raised when a file cannot be copied to the system clipboard."""


def copy_file_to_clipboard(file_path: str | Path) -> None:
    """Copy a file reference to the OS clipboard using a platform-specific backend."""
    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise ClipboardFileCopyError(f'File does not exist: {path}')

    system = platform.system()

    if system == 'Darwin':
        _copy_file_macos(path)
        return

    if system == 'Windows':
        _copy_file_windows(path)
        return

    if system == 'Linux':
        _copy_file_linux(path)
        return

    raise ClipboardFileCopyError(f'Unsupported platform: {system}')


def _copy_file_macos(path: Path) -> None:
    script = f"""
    tell application "Finder"
        set the clipboard to (POSIX file "{path}")
    end tell
    """
    try:
        subprocess.run(
            ['osascript', '-e', script],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise ClipboardFileCopyError(exc.stderr.strip() or str(exc)) from exc


def _copy_file_windows(path: Path) -> None:
    script = rf"""
Add-Type -AssemblyName System.Windows.Forms
$fileDropList = New-Object System.Collections.Specialized.StringCollection
$fileDropList.Add("{path}") | Out-Null
[System.Windows.Forms.Clipboard]::SetFileDropList($fileDropList)
"""
    try:
        subprocess.run(
            ['powershell', '-NoProfile', '-STA', '-Command', script],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise ClipboardFileCopyError(exc.stderr.strip() or str(exc)) from exc
    except FileNotFoundError as exc:
        raise ClipboardFileCopyError(
            'PowerShell was not found. File clipboard is unavailable on this Windows environment.'
        ) from exc


def _copy_file_linux(path: Path) -> None:
    uri_list = f'{path.as_uri()}\n'

    backends = [
        ['wl-copy', '--type', 'text/uri-list'],
        ['xclip', '-selection', 'clipboard', '-t', 'text/uri-list'],
        ['xsel', '--clipboard', '--input'],
    ]

    last_error: Exception | None = None

    for cmd in backends:
        try:
            subprocess.run(
                cmd,
                input=uri_list,
                check=True,
                capture_output=True,
                text=True,
            )
            return
        except FileNotFoundError as exc:
            last_error = exc
            continue
        except subprocess.CalledProcessError as exc:
            raise ClipboardFileCopyError(exc.stderr.strip() or str(exc)) from exc

    raise ClipboardFileCopyError(
        'No supported Linux clipboard backend found. Install one of: wl-clipboard, xclip, or xsel.'
    ) from last_error
