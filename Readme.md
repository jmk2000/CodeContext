# CodeContext 🧠

A simple, powerful command-line tool to recursively scan a project directory, concatenate all relevant source code and configuration files, and dump the database schema into a single, clean text file. This file is perfectly formatted to be fed into a Large Language Model (LLM) like GPT-4, Claude, or Gemini, providing it with the full context of your project for debugging, analysis, or documentation tasks.

## Key Features ✨

* **Comprehensive Context**: Gathers source code, config files (`.env`, `Dockerfile`, `*.yml`), and more.
* **Smart Filtering**: Intelligently ignores unnecessary files and directories like `node_modules`, `.git`, and build artifacts to save tokens and reduce noise.
* **Database Schema Dumping**: Automatically detects database services in `docker-compose.yml` (PostgreSQL, MySQL, SQLite) and includes the schema in the output.
* **Secret Redaction**: Automatically finds and redacts sensitive information like passwords and API keys from your config files.
* **Multiple Formats**: Choose your output format - **Markdown** (default), **XML**, or a token-efficient **Minimal** text format.
* **Easy to Use**: Run it with a single command from your project's root directory.

## Installation 📦

You can install `CodeContext` via pip once it is published to PyPI. For now, you can install it directly from the Git repository:

```bash
pip install git+[https://github.com/your-username/CodeContext.git](https://github.com/your-username/CodeContext.git)
```

Additionally, for database schema dumping, you must have the appropriate command-line tools installed and available in your system's `PATH`:
* **PostgreSQL**: `pg_dump`
* **MySQL**: `mysqldump`
* **SQLite**: `sqlite3`

## Usage 🚀

The simplest way to use `CodeContext` is to run it in the root directory of your project.

```bash
# This will scan the current directory and create 'code_context.md'
codecontext
```

### Command-Line Options

You can customize the behavior with the following options:

| Option                 | Shorthand | Description                                                                | Default                               |
| ---------------------- | --------- | -------------------------------------------------------------------------- | ------------------------------------- |
| `root_dir`             | (none)    | The project directory to scan.                                             | `.` (current directory)               |
| `--output <file>`      | `-o`      | The path for the output file.                                              | `code_context.[md\|xml\|txt]`         |
| `--format <format>`    | `-f`      | The output format. Choices: `markdown`, `xml`, `minimal`.                  | `markdown`                            |
| `--no-db`              |           | A flag to disable the database schema dump.                                | (not set)                             |

### Examples

**Scan a different directory and specify an output file:**

```bash
codecontext /path/to/my-other-project -o my_project_context.md
```

**Generate an XML output:**

```bash
codecontext -f xml
# This will create 'code_context.xml'
```

**Skip the database schema check:**

```bash
codecontext --no-db
```

## How to Use with an LLM 🤖

1.  Run `codecontext` in your project.
2.  Open the generated output file (e.g., `code_context.md`).
3.  **IMPORTANT**: Quickly review the file to ensure no sensitive data was accidentally included.
4.  Copy and paste the entire content into your chat session with an LLM.
5.  Start your prompt with something like:
    > "I'm providing you with the full context of my software project, including all relevant source code, configuration files, and the database schema. Please act as an expert software developer and help me with the following task.
    >
    > [Your question or debugging request here]"

## Contributing 🤝

Contributions are welcome! If you have suggestions for improvements, please open an issue or submit a pull request.

## License 📄

This project is licensed under the MIT License. See the LICENSE file for details.