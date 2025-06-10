# codecontext/formatters.py
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

class BaseFormatter(ABC):
    @abstractmethod
    def format_header(self) -> str:
        pass

    @abstractmethod
    def format_file(self, path: str, content: str) -> str:
        pass

    @abstractmethod
    def format_db_schema(self, db_type: str, db_name: str, schema: str) -> str:
        pass

    @abstractmethod
    def format_footer(self) -> str:
        pass

class MarkdownFormatter(BaseFormatter):
    def format_header(self) -> str:
        return "# CodeContext Report\n\n"

    def format_file(self, path: str, content: str) -> str:
        lang = path.split('.')[-1]
        return f"## File: `{path}`\n\n```{lang}\n{content}\n```\n\n"

    def format_db_schema(self, db_type: str, db_name: str, schema: str) -> str:
        return f"## Database Schema: `{db_type} ({db_name})`\n\n```sql\n{schema}\n```\n\n"

    def format_footer(self) -> str:
        return "---\n*End of Report*"

class XmlFormatter(BaseFormatter):
    def __init__(self):
        self.root = ET.Element("CodeContext")

    def format_header(self) -> str:
        return "" # Handled at the end

    def format_file(self, path: str, content: str) -> str:
        file_element = ET.SubElement(self.root, "File")
        file_element.set("path", path)
        file_element.text = content
        return "" # Appended to root, not returned as string

    def format_db_schema(self, db_type: str, db_name: str, schema: str) -> str:
        db_element = ET.SubElement(self.root, "DatabaseSchema")
        db_element.set("type", db_type)
        db_element.set("name", db_name)
        db_element.text = schema
        return ""

    def format_footer(self) -> str:
        # Pretty print the XML
        ET.indent(self.root)
        return ET.tostring(self.root, encoding="unicode")

class MinimalFormatter(BaseFormatter):
    def format_header(self) -> str:
        return ""

    def format_file(self, path: str, content: str) -> str:
        return f"---\nFile: {path}\n---\n{content}\n"

    def format_db_schema(self, db_type: str, db_name: str, schema: str) -> str:
        return f"---\nDatabase Schema: {db_type} ({db_name})\n---\n{schema}\n"

    def format_footer(self) -> str:
        return ""

def get_formatter(format_name: str) -> BaseFormatter:
    """Factory function to get the appropriate formatter."""
    if format_name == 'xml':
        return XmlFormatter()
    if format_name == 'minimal':
        return MinimalFormatter()
    return MarkdownFormatter() # Default