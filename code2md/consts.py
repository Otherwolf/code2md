PYTHON_DEFAULT_EXCLUDED_DIRS = {
    '__pycache__',
    '.venv',
    'venv',
    'env',
    '.eggs',
    '.egg-info',
    '*.egg-info',
    '.mypy_cache',
    '.pytest_cache',
    '.ruff_cache',
    '.tox',
    '.nox',
    'htmlcov',
    'build',
    'dist',
    'site',
    'pip-wheel-metadata',
}

PYTHON_DEFAULT_EXCLUDED_FILES = {
    'pip-freeze.txt',
    'requirements.txt',
}

PYTHON_DEFAULT_EXCLUDED_EXTENSIONS = {
    '.pyc',
    '.pyo',
    '.so',
    '.lock',
}

FRONTEND_DEFAULT_EXCLUDED_DIRS = {
    'node_modules',
    '.next',
    '.nuxt',
    '.svelte-kit',
    '.parcel-cache',
    '.turbo',
    '.vercel',
    'coverage',
    'out',
    'public',
    'static',
    'dist',
    'build',
}

FRONTEND_DEFAULT_EXCLUDED_FILES = {
    'package-lock.json',
    'yarn.lock',
    'pnpm-lock.yaml',
    'bun.lockb',
    'next-env.d.ts',
}

FRONTEND_DEFAULT_EXCLUDED_EXTENSIONS = {
    '.log',
    '.tmp',
    '.lock',
    '.tsbuildinfo',
}

GENERAL_EXCLUDED_DIRS = {
    '.git',
    '.svn',
    '.hg',
    '.idea',
    '.vscode',
}

GENERAL_EXCLUDED_FILES = {
    '.DS_Store',
    'Thumbs.db',
    '.coverage',
    'coverage.xml',
}

GENERAL_EXCLUDED_EXTENSIONS = {
    '.sqlite3',
}

LANGUAGE_MAP = {
    # Python
    '.py': 'python',
    '.pyi': 'python',
    '.pyx': 'python',
    # JavaScript/TypeScript
    '.js': 'javascript',
    '.ts': 'typescript',
    '.mjs': 'javascript',
    '.cjs': 'javascript',
    # HTML/CSS
    '.html': 'html',
    '.htm': 'html',
    '.xhtml': 'html',
    '.css': 'css',
    '.scss': 'scss',
    '.sass': 'sass',
    '.less': 'less',
    # Markup languages
    '.xml': 'xml',
    '.json': 'json',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.md': 'markdown',
    '.markdown': 'markdown',
    # Shell/Config
    '.sh': 'bash',
    '.bash': 'bash',
    '.zsh': 'bash',
    '.fish': 'bash',
    '.bat': 'batch',
    '.cmd': 'batch',
    '.ps1': 'powershell',
    # C/C++
    '.c': 'c',
    '.h': 'c',
    '.cpp': 'cpp',
    '.hpp': 'cpp',
    '.cc': 'cpp',
    '.cxx': 'cpp',
    '.hh': 'cpp',
    # C#
    '.cs': 'csharp',
    '.csx': 'csharp',
    # Java
    '.java': 'java',
    '.jsp': 'jsp',
    # Go
    '.go': 'go',
    # Rust
    '.rs': 'rust',
    # PHP
    '.php': 'php',
    '.phtml': 'php',
    '.php3': 'php',
    '.php4': 'php',
    '.php5': 'php',
    '.php7': 'php',
    '.php8': 'php',
    # Ruby
    '.rb': 'ruby',
    '.erb': 'erb',
    '.rake': 'ruby',
    # SQL
    '.sql': 'sql',
    # Swift
    '.swift': 'swift',
    # Kotlin
    '.kt': 'kotlin',
    '.kts': 'kotlin',
    # Scala
    '.scala': 'scala',
    '.sc': 'scala',
    # R
    '.r': 'r',
    '.R': 'r',
    # MATLAB
    '.m': 'matlab',
    # Lua
    '.lua': 'lua',
    # Perl
    '.pl': 'perl',
    '.pm': 'perl',
    '.t': 'perl',
    # Dart
    '.dart': 'dart',
    # Objective-C
    '.m': 'objectivec',
    '.mm': 'objectivec',
    # Docker
    'Dockerfile': 'dockerfile',
    '.dockerfile': 'dockerfile',
    # Make
    'Makefile': 'makefile',
    'makefile': 'makefile',
    '.mk': 'makefile',
    # Ini/Config
    '.ini': 'ini',
    '.cfg': 'ini',
    '.conf': 'ini',
    '.toml': 'toml',
    # Diff
    '.diff': 'diff',
    '.patch': 'diff',
    # GraphQL
    '.graphql': 'graphql',
    '.gql': 'graphql',
    # Vue
    '.vue': 'vue',
    # React
    '.jsx': 'jsx',
    '.tsx': 'tsx',
}
