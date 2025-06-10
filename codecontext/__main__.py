# codecontext/__main__.py
import argparse
import os
from . import file_handler, db_handler, formatters
from .config import EXCLUDE_DIRS, EXCLUDE_FILES, INCLUDE_EXTENSIONS

def main():
    parser = argparse.ArgumentParser(
        description="Gather project context for LLM analysis."
    )
    parser.add_argument(
        "root_dir",
        nargs="?",
        default=".",
        help="The root directory of the project to scan. Defaults to current directory.",
    )
    parser.add_argument(
        "-o", "--output",
        help="The path to the output file. Defaults to 'code_context.[ext]' in the root directory.",
    )
    parser.add_argument(
        "-f", "--format",
        choices=['markdown', 'xml', 'minimal'],
        default='markdown',
        help="The output format for the context file.",
    )
    parser.add_argument(
        "--no-db",
        action="store_true",
        help="Skip automatic database schema dumping.",
    )
    args = parser.parse_args()

    formatter = formatters.get_formatter(args.format)
    
    # Determine output file path
    output_file = args.output
    if not output_file:
        ext_map = {'markdown': 'md', 'xml': 'xml', 'minimal': 'txt'}
        output_file = f"code_context.{ext_map[args.format]}"

    print(f"Scanning project in: {os.path.abspath(args.root_dir)}")
    print(f"Output format: {args.format}")
    
    # 1. Gather all source files
    source_files = file_handler.get_project_files(
        args.root_dir, EXCLUDE_DIRS, EXCLUDE_FILES, INCLUDE_EXTENSIONS
    )
    
    # 2. Attempt to get DB schema
    db_schema_content = ""
    if not args.no_db:
        compose_file = db_handler.find_docker_compose(args.root_dir)
        if compose_file:
            print(f"Found docker-compose file: {compose_file}")
            db_info = db_handler.get_db_connection_from_docker(compose_file)
            if db_info:
                schema = db_handler.get_db_schema(db_info)
                if schema:
                    db_schema_content = formatter.format_db_schema(
                        db_info['type'], db_info['dbname'], schema
                    )
            else:
                print("Could not find a supported database service in docker-compose.yml.")
        else:
            print("No docker-compose.yml found. Skipping database schema dump.")

    # 3. Format and write the output
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatter.format_header())
            
            for path, content in sorted(source_files):
                print(f"  + Adding file: {path}")
                f.write(formatter.format_file(path, content))

            if db_schema_content:
                print("  + Adding database schema.")
                f.write(db_schema_content)
                
            f.write(formatter.format_footer())

        print(f"\n✅ Success! Project context saved to: {output_file}")

    except IOError as e:
        print(f"\n❌ Error: Could not write to output file {output_file}: {e}")

if __name__ == "__main__":
    main()