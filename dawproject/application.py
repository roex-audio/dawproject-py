"""Application model -- identifies the application that created the project."""

from lxml import etree as ET


class Application:
    """Identifies the application that created this DAWproject file.

    Attributes:
        name: Application name.
        version: Application version string.
    """

    def __init__(self, name=None, version=None):
        self.name = name
        self.version = version

    def to_xml(self):
        application_elem = ET.Element("Application")
        if self.name:
            application_elem.set("name", self.name)
        if self.version:
            application_elem.set("version", self.version)
        return application_elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return cls()
        name = element.get("name")
        version = element.get("version")
        return cls(name, version)
