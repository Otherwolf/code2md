# code2md

`code2md` is a small, focused CLI tool that walks your project tree and compiles both the structure and file contents into a single Markdown document. This is particularly useful for preparing context for LLMs, creating lightweight documentation, or archiving codebases in a text‑friendly format.

## 🚀 Features

- **Project tree rendering**: Produces a readable, indented directory tree with file entries.  
- **Inline file contents**: Embeds source files directly into the Markdown output, with syntax highlighting inferred from extensions and common filenames.  
- **Fine‑grained exclusions**: Lets you control exactly which files and directories are included via directory/file/extension filters.  
- **Built‑in presets**: Ships with sensible exclusion sets for Python and frontend projects (e.g. virtualenvs, caches, `node_modules`, build artifacts).  
- **Single CLI entrypoint**: Exposed as a single `code2md` command with straightforward flags, easy to integrate into existing workflows.  
- **Optional clipboard integration**: Can copy the generated Markdown file to the system clipboard via a platform‑specific helper (macOS / Windows / Linux).

---

## 📦 Global CLI installation

`code2md` is distributed as a standard Python package with a `console_scripts` entry point that exposes the `code2md` command.  
Requires **Python 3.7+**.

### Option 1. Install directly from GitHub (recommended)

```bash
# Install into the current Python environment (system or virtualenv)
python3 -m pip install "git+https://github.com/Otherwolf/code2md.git"
```

After installation, the CLI should be available:

```bash
code2md --help
```

### Option 2. Install from a local clone

```bash
git clone https://github.com/Otherwolf/code2md.git
cd code2md
python3 -m pip install .
```

For active development, install in editable mode:

```bash
python3 -m pip install -e .
```

### Option 3. Install as an isolated global CLI via pipx

If you prefer to keep your global Python site‑packages clean, you can install `code2md` with `pipx`:

```bash
pipx install "git+https://github.com/Otherwolf/code2md.git"
```

This makes `code2md` available on your `PATH` as a standalone command, independent of any virtual environment.

---

## ✅ Verifying the installation

Run:

```bash
code2md --help
```

You should see the CLI help and argument list implemented in `code2md.main:main`.

---

## 🚀 Quick start

Generate a Markdown snapshot of the current project:

```bash
code2md .
```

Write the result to a dedicated output directory:

```bash
code2md . -o ./docs
```

Use the built‑in Python defaults:

```bash
code2md . --add-python-defaults
```

By default, `code2md` creates a file named `<folder_name>_structure.md` that contains the directory tree and file contents in Markdown format.

---

## 📋 Copying the generated file to the clipboard

You can ask `code2md` to copy the generated Markdown file itself to the system clipboard using the `--copy` flag:

```bash
code2md . --add-python-defaults --copy
```

Under the hood, `code2md` uses a small platform‑specific helper:

- **macOS** – AppleScript via Finder (`osascript`) to put the file into the clipboard.  
- **Windows** – PowerShell and `System.Windows.Forms.Clipboard.SetFileDropList` to publish a file drop list.  
- **Linux** – `text/uri-list` written to the clipboard via one of `wl-copy`, `xclip`, or `xsel` (the first available backend).

> Note: whether a particular browser or web application will accept `Cmd/Ctrl+V` as “paste file” depends on the OS, browser, and the site’s clipboard handling. The helper publishes a file reference to the OS clipboard, but the exact paste behavior is still environment‑dependent.

---

## 🛠️ Usage

From the root of the project you want to export, run:

### Basic example

```bash
code2md
```

This will produce a file `project_<folder_name>_structure.md` in the current directory. Out of the box, `code2md` will:

- Skip common VCS and IDE directories such as `.git`, `.svn`, `.hg`, `.idea`, `.vscode`.  
- Exclude all “dot‑files” and “dot‑directories” (anything starting with `.` such as `.env`, `.github`).  

### Advanced examples

**1. Python + frontend project**

Use the presets to ignore typical noise for both stacks:

```bash
code2md --add-python-defaults --add-frontend-defaults
```

This adds exclusions for things like `__pycache__`, `venv`, `node_modules`, `.next`, build outputs and various cache directories.

**2. Custom exclusions on top of presets**

You can combine presets with your own rules.  
For example, also exclude `migrations` and `config.local.js`:

```bash
code2md --add-python-defaults -d "migrations" -f "config.local.js"
```

**3. Including dotfiles in the report**

If you need files like `.env` or `.github/workflows/main.yml` in the output, disable the default dotfile exclusion:

```bash
code2md --no-exclude-dotfiles --add-python-defaults
```

**4. Generate and immediately prepare the file for paste**

Typical “generate and paste into browser” flow:

```bash
code2md . --add-python-defaults --add-frontend-defaults --copy
```

If the target browser/web app supports pasting files from the clipboard, `Cmd/Ctrl+V` should then offer the generated Markdown file.

### CLI arguments

The CLI exposes a small, explicit set of flags:

| Flag                         | Description                                                                                   | Example                                |
| :--------------------------- | :-------------------------------------------------------------------------------------------- | :------------------------------------- |
| `project_path`               | Optional path to the project root. Defaults to the current directory.                        | `code2md ../my-other-project`         |
| `-o`, `--output-dir`         | Output directory for the generated Markdown file.                                            | `code2md -o "output/docs"`            |
| `-d`, `--exclude-dirs`       | Comma‑separated list of directories to exclude.                                              | `code2md -d ".git,build"`             |
| `-f`, `--exclude-files`      | Comma‑separated list of filenames to exclude.                                                | `code2md -f ".env,config.local.json"` |
| `-e`, `--exclude-extensions` | Comma‑separated list of file extensions to exclude (with or without leading dot).           | `code2md -e ".log,.tmp"`              |
| `--add-python-defaults`      | Add the built‑in Python exclusion set (`__pycache__`, virtualenvs, coverage artifacts, etc.).| `code2md --add-python-defaults`       |
| `--add-frontend-defaults`    | Add the built‑in frontend exclusion set (`node_modules`, `.next`, build outputs, etc.).     | `code2md --add-frontend-defaults`     |
| `--no-exclude-dotfiles`      | Include files and directories starting with `.` (dotfiles) in the output.                   | `code2md --no-exclude-dotfiles`       |
| `--copy`                     | Copy the generated Markdown file to the system clipboard (platform‑specific implementation). | `code2md . --copy`                    |
| `-v`, `--verbose`            | Enable verbose logging, including effective exclusion sets and visited paths.               | `code2md -v`                          |

### Exclusion strategy

`code2md` applies exclusions in clearly defined layers:

1. **Base exclusions**: Always skips generic VCS and IDE directories such as `.git`, `.svn`, `.hg`, `.idea`, `.vscode`.  
2. **Dotfiles**: By default, any file or directory whose name starts with `.` is excluded; this can be overridden via `--no-exclude-dotfiles`.  
3. **Presets**: `--add-python-defaults` and `--add-frontend-defaults` extend the exclusion lists with language‑specific noise (caches, build outputs, lockfiles, etc.).  
4. **User overrides**: Arguments passed via `-d`, `-f`, and `-e` are merged into the corresponding exclusion sets, allowing you to tailor the final report to your project’s needs.
