"""FileReference model -- a reference to a file (internal or external)."""

from lxml import etree as ET


class FileReference:
    """A reference to a file, either embedded or external.

    Attributes:
        path: The file path.
        external: Whether the file is external to the archive.
    """

    def __init__(self, path="", external=False):
        self.path = path
        self.external = external

    def to_xml(self):
        file_elem = ET.Element("File")
        file_elem.set("path", self.path)
        file_elem.set("external", str(self.external).lower())
        return file_elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return cls()
        path = element.get("path", "")
        external = element.get("external")
        external = external.lower() == "true" if external else False
        return cls(path, external)
