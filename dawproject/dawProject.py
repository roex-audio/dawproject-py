"""Core DawProject class for loading, saving, and validating DAWproject files."""

from pathlib import Path
from lxml import etree as ET
from zipfile import ZipFile
from io import BytesIO


FORMAT_NAME = "DAWproject exchange format"
FILE_EXTENSION = "dawproject"

PROJECT_FILE = "project.xml"
METADATA_FILE = "metadata.xml"


class DawProject:
    """Main entry point for working with DAWproject files.

    Provides static methods for saving and loading .dawproject files
    (ZIP archives containing project.xml, metadata.xml, and embedded audio),
    as well as standalone XML export and schema validation.
    """

    FORMAT_NAME = "DAWproject exchange format"
    FILE_EXTENSION = "dawproject"
    PROJECT_FILE = "project.xml"
    METADATA_FILE = "metadata.xml"

    @staticmethod
    def save_xml(project, file):
        """Save a Project as a standalone XML file.

        Args:
            project: A Project instance to serialize.
            file: Path to the output XML file.
        """
        from .project import Project

        root = project.to_xml()
        tree = ET.ElementTree(root)
        with open(file, "wb") as file_out:
            tree.write(file_out, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    @staticmethod
    def save(project, metadata, embedded_files, file):
        """Save a full .dawproject archive (ZIP with project.xml, metadata.xml, and embedded files).

        Args:
            project: A Project instance to serialize.
            metadata: A MetaData instance to serialize.
            embedded_files: Dict mapping file content (bytes) to path-in-zip (str).
            file: Path to the output .dawproject file.
        """
        # Serialize project
        project_root = project.to_xml()
        project_xml = ET.tostring(project_root, pretty_print=True, xml_declaration=True, encoding="UTF-8")

        # Serialize metadata
        metadata_root = metadata.to_xml()
        metadata_xml = ET.tostring(metadata_root, pretty_print=True, xml_declaration=True, encoding="UTF-8")

        with ZipFile(file, "w") as zos:
            DawProject._add_to_zip(zos, DawProject.METADATA_FILE, metadata_xml)
            DawProject._add_to_zip(zos, DawProject.PROJECT_FILE, project_xml)
            for data, path_in_zip in embedded_files.items():
                DawProject._add_to_zip(zos, path_in_zip, data)

    @staticmethod
    def _add_to_zip(zos, path, data):
        """Write data to a path within a ZipFile."""
        with zos.open(path, "w") as entry:
            entry.write(data)

    @staticmethod
    def validate(project):
        """Validate a Project against the DAWproject XML schema.

        Args:
            project: A Project instance to validate.

        Raises:
            IOError: If validation fails or the schema cannot be loaded.
        """
        try:
            root = project.to_xml()
            project_xml = ET.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")

            # Resolve schema path relative to this package
            schema_path = Path(__file__).parent.parent / "Project.xsd"
            with open(schema_path, "r") as schema_file:
                schema_doc = ET.parse(schema_file)
                schema = ET.XMLSchema(schema_doc)

            xml_doc = ET.parse(BytesIO(project_xml))
            schema.assertValid(xml_doc)

        except ET.XMLSchemaError as e:
            raise IOError(f"Schema validation error: {e}")
        except Exception as e:
            raise IOError(f"Unexpected error: {e}")

    @staticmethod
    def load_project(file):
        """Load a Project from a .dawproject file.

        Args:
            file: Path to the .dawproject file.

        Returns:
            A Project instance populated from the file.
        """
        from .project import Project

        with ZipFile(file, "r") as zip_file:
            data = zip_file.read(DawProject.PROJECT_FILE)
            # Strip BOM if present
            if data[:3] == b'\xef\xbb\xbf':
                data = data[3:]
            root = ET.fromstring(data)
            return Project.from_xml(root)

    # Alias for convenience
    load = load_project

    @staticmethod
    def load_metadata(file):
        """Load MetaData from a .dawproject file.

        Args:
            file: Path to the .dawproject file.

        Returns:
            A MetaData instance populated from the file.
        """
        from .metaData import MetaData

        with ZipFile(file, "r") as zip_file:
            entry = zip_file.open(DawProject.METADATA_FILE)
            data = entry.read()
            # Strip BOM if present
            if data[:3] == b'\xef\xbb\xbf':
                data = data[3:]
            root = ET.fromstring(data)
            return MetaData.from_xml(root)

    @staticmethod
    def stream_embedded(file, embedded_path):
        """Read an embedded file from a .dawproject archive.

        Args:
            file: Path to the .dawproject file.
            embedded_path: Path of the embedded file within the archive.

        Returns:
            A file-like BytesIO object for reading the embedded file.
        """
        with ZipFile(file, "r") as zip_file:
            return BytesIO(zip_file.read(embedded_path))
