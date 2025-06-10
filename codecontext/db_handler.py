# codecontext/db_handler.py
import os
import yaml
import time
import subprocess
from typing import Optional, Dict, Any

def find_docker_compose(root_dir: str) -> Optional[str]:
    """Find docker-compose.yml in the root directory."""
    for filename in ["docker-compose.yml", "docker-compose.yaml"]:
        path = os.path.join(root_dir, filename)
        if os.path.exists(path):
            return path
    return None

def get_db_connection_from_docker(
    compose_file: str
) -> Optional[Dict[str, Any]]:
    """Parse docker-compose file to find database service details."""
    try:
        with open(compose_file, 'r') as f:
            compose_data = yaml.safe_load(f)
    except Exception:
        return None

    for service_name, service in compose_data.get('services', {}).items():
        image = service.get('image', '').lower()
        if 'postgres' in image:
            db_type = 'postgresql'
        elif 'mysql' in image:
            db_type = 'mysql'
        elif 'sqlite' in image:
            db_type = 'sqlite'
        else:
            continue

        env = service.get('environment', {})
        return {
            "type": db_type,
            "host": service_name, # Service name is the hostname in Docker network
            "port": list(service.get('ports', ['5432:5432']))[0].split(':')[0],
            "user": env.get('POSTGRES_USER') or env.get('MYSQL_USER'),
            "password": env.get('POSTGRES_PASSWORD') or env.get('MYSQL_PASSWORD'),
            "dbname": env.get('POSTGRES_DB') or env.get('MYSQL_DATABASE'),
        }
    return None

def get_db_schema(db_info: Dict[str, Any]) -> Optional[str]:
    """Dumps the schema for a given database type."""
    db_type = db_info["type"]
    print(f"Attempting to dump schema for {db_type} database...")

    # For SQLite, the 'dbname' is the file path
    if db_type == 'sqlite':
        db_file = db_info.get("dbname")
        if not db_file or not os.path.exists(db_file):
            print(f"Warning: SQLite database file not found at {db_file}")
            return None
        try:
            result = subprocess.run(
                ['sqlite3', db_file, '.schema'],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except Exception as e:
            print(f"Warning: Failed to dump SQLite schema: {e}")
            return None
            
    # For PostgreSQL, use pg_dump
    if db_type == 'postgresql':
        os.environ['PGPASSWORD'] = db_info['password']
        cmd = [
            'pg_dump',
            '--schema-only',
            '-h', db_info['host'],
            '-p', str(db_info['port']),
            '-U', db_info['user'],
            db_info['dbname']
        ]
        try:
            # Assumes pg_dump is in PATH and the container is running
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except Exception as e:
            print(f"Warning: Failed to dump PostgreSQL schema. Is the container running and pg_dump installed? Error: {e}")
            return None
        finally:
            del os.environ['PGPASSWORD']
            
    # For MySQL, use mysqldump
    if db_type == 'mysql':
        cmd = [
            'mysqldump',
            '--no-data',
            '--skip-opt',
            '--host', db_info['host'],
            '--port', str(db_info['port']),
            '--user', db_info['user'],
            f"--password={db_info['password']}",
            db_info['dbname']
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except Exception as e:
            print(f"Warning: Failed to dump MySQL schema. Is the container running and mysqldump installed? Error: {e}")
            return None

    return None