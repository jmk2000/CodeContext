# codecontext/file_handler.py
import os
import fnmatch
from pathlib import Path
from typing import Set, List, Tuple

from .config import INCLUDE_EXTENSIONS, INCLUDE_FILES, EXCLUDE_DIRS, EXCLUDE_FILES
from .secrets_redactor import redact_secrets

def get_project_files(
    root_dir: str,
    exclude_dirs: Set[str],
    exclude_files: Set[str],
    include_ext: Set[str],
) -> List[Tuple[str, str]]:
    """
    Recursively finds and reads files, applying inclusion/exclusion rules.
    """
    source_files = []
    root_path = Path(root_dir).resolve()

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=True):
        # Modify dirnames in-place to prune unwanted directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for filename in filenames:
            file_path = Path(dirpath) / filename
            rel_path = file_path.relative_to(root_path)

            # Check exclusion rules
            if any(fnmatch.fnmatch(str(rel_path), p) for p in exclude_files):
                continue

            # Check inclusion rules
            is_included_ext = file_path.suffix in include_ext
            is_included_file = filename.lower() in INCLUDE_FILES

            if is_included_ext or is_included_file:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Redact secrets before adding
                    content = redact_secrets(content, filename)
                    source_files.append((str(rel_path), content))
                    
                except Exception as e:
                    print(f"Warning: Could not read file {file_path}: {e}")

    return source_files