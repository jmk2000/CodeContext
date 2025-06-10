# codecontext/config.py

# Default configuration for file and directory filtering.
# Based on user-provided JSON.

# Set of file extensions to include in the context
INCLUDE_EXTENSIONS = {
    # Programming languages
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.cc', '.cxx',
    '.h', '.hpp', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
    '.clj', '.hs', '.ml', '.fs', '.vb', '.pas', '.ada', '.lua', '.pl', '.r',
    '.m', '.mm', '.dart', '.elm', '.ex', '.exs', '.jl', '.nim', '.cr', '.zig',
    # Web technologies
    '.html', '.htm', '.css', '.scss', '.sass', '.less', '.vue', '.svelte',
    '.xml', '.xsl', '.xslt', '.svg',
    # Configuration and data
    '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.properties',
    '.env', '.dockerfile', '.tf', '.hcl', '.nomad',
    # Documentation
    '.md', '.rst', '.txt', '.asciidoc', '.adoc',
    # Build and deployment
    '.cmake', '.make', '.gradle', '.sbt', '.rakefile',
    # Scripts
    '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd',
    # Database
    '.sql', '.psql', '.mysql', '.sqlite'
}

# Set of exact filenames to include
INCLUDE_FILES = {
    'dockerfile', 'makefile', 'rakefile', 'gemfile', 'pipfile', 'poetry.lock',
    'package.json', 'composer.json', 'requirements.txt', 'setup.py', 'pyproject.toml'
}

# Set of directory names to exclude from search
EXCLUDE_DIRS = {
    # Version control
    '.git', '.svn', '.hg', '.bzr',
    # IDE and editor files
    '.vscode', '.idea', '.vs', '__pycache__', '.pytest_cache',
    # Dependencies and packages
    'node_modules', 'vendor', 'packages', 'bower_components', 'venv', 'env',
    # Build outputs
    'build', 'dist', 'out', 'target', 'bin', 'obj', '.next', '.nuxt',
    # Temporary and cache
    'tmp', 'temp', '.cache', '.parcel-cache', '.webpack',
    # OS specific
    '.DS_Store', 'Thumbs.db',
    # Logs
    'logs', 'log'
}

# Set of filenames (with wildcards) to exclude
EXCLUDE_FILES = {
    '*.pyc', '*.pyo', '*.class', '*.o', '*.so', '*.dylib', '*.dll',
    '*.zip', '*.tar', '*.gz', '*.7z', '*.rar',
    '*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.ico',
    '*.mp3', '*.mp4', '*.avi', '*.mov', '*.wmv',
    '*.pdf', '*.doc', '*.docx', '*.xls', '*.xlsx', '*.ppt', '*.pptx',
    '*.log', '*.out', '*.err',
    '*.tmp', '*.temp', '*.swp', '*.swo', '*~',
    '.DS_Store', 'Thumbs.db', 'desktop.ini',
    'poetry.lock', 'package-lock.json' # Often too verbose
}