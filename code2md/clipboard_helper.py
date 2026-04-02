from __future__ import annotations

import os
from pathlib import Path
import platform
import shutil
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
    wayland_display = os.environ.get('WAYLAND_DISPLAY')
    x_display = os.environ.get('DISPLAY')

    backends: list[list[str]] = []

    if wayland_display and shutil.which('wl-copy'):
        backends.append(['wl-copy', '--type', 'text/uri-list'])

    if x_display:
        if shutil.which('xclip'):
            backends.append(['xclip', '-selection', 'clipboard', '-t', 'text/uri-list'])
        if shutil.which('xsel'):
            backends.append(['xsel', '--clipboard', '--input'])

    if not backends:
        if not wayland_display and not x_display:
            raise ClipboardFileCopyError(
                'No graphical clipboard session found on Linux. '
                'WAYLAND_DISPLAY and DISPLAY are unset.'
            )

        raise ClipboardFileCopyError(
            'No supported Linux clipboard backend found for the current session. '
            'Install wl-clipboard for Wayland, or xclip/xsel for X11.'
        )

    errors: list[str] = []

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
        except subprocess.CalledProcessError as exc:
            errors.append(f'{" ".join(cmd)}: {exc.stderr.strip() or str(exc)}')

    raise ClipboardFileCopyError(' ; '.join(errors))
