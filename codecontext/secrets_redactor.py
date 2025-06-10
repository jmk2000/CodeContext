# codecontext/secrets_redactor.py
import re

# Common patterns for keys that might hold secrets
SECRET_KEY_PATTERNS = [
    'password', 'secret', 'token', 'api_key', 'credential',
    'access_key', 'private_key'
]

# Regex to find assignments of keys in .env or config files
# Catches: KEY=VALUE, KEY="VALUE", KEY='VALUE'
ENV_VAR_REGEX = re.compile(
    r"^(?P<key>[\w\.\-_]+)\s*=\s*['\"]?(?P<value>.+?)['\"]?$", re.MULTILINE
)

def redact_secrets(content: str, filename: str) -> str:
    """
    Redacts sensitive values in a given file's content.
    Especially useful for .env, .yml, or configuration files.
    """
    if not any(filename.endswith(ext) for ext in ['.env', '.yml', '.yaml', '.json']):
        return content

    redacted_lines = []
    lines = content.split('\n')

    for line in lines:
        match = ENV_VAR_REGEX.match(line)
        if match:
            key = match.group('key').lower()
            if any(p in key for p in SECRET_KEY_PATTERNS):
                redacted_lines.append(f"{match.group('key')}=[REDACTED]")
                continue
        redacted_lines.append(line)

    return "\n".join(redacted_lines)