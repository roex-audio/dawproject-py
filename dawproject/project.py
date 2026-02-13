"""Project model -- the top-level container for a DAWproject file."""

from lxml import etree as ET
from .application import Application
from .transport import Transport
from .lane import Lane
from .arrangement import Arrangement
from .scene import Scene


class Project:
    """Top-level DAWproject model containing structure, arrangement, and metadata.

    Attributes:
        version: The DAWproject format version (default "1.0").
        application: An Application instance identifying the creating software.
        transport: A Transport instance with tempo and time signature.
        structure: A list of Track and/or Channel objects.
        arrangement: An Arrangement instance with timeline content.
        scenes: A list of Scene objects.
    """

    CURRENT_VERSION = "1.0"

    def __init__(
        self,
        version=None,
        application=None,
        transport=None,
        structure=None,
        arrangement=None,
        scenes=None,
    ):
        self.version = version if version else self.CURRENT_VERSION
        self.application = application if application else Application()
        self.transport = transport
        self.structure = structure if structure else []
        self.arrangement = arrangement
        self.scenes = scenes if scenes else []

    def to_xml(self):
        """Serialize this Project to an lxml Element."""
        root = ET.Element("Project", version=self.version)

        # Application element
        app_elem = self.application.to_xml()
        root.append(app_elem)

        if self.transport:
            root.append(self.transport.to_xml())

        if self.structure:
            structure_elem = ET.SubElement(root, "Structure")
            for lane in self.structure:
                structure_elem.append(lane.to_xml())

        if self.arrangement:
            root.append(self.arrangement.to_xml())

        if self.scenes:
            scenes_elem = ET.SubElement(root, "Scenes")
            for scene in self.scenes:
                scenes_elem.append(scene.to_xml())

        return root

    @classmethod
    def from_xml(cls, element):
        """Deserialize a Project from an lxml Element."""
        from .track import Track
        from .channel import Channel

        version = element.get("version", cls.CURRENT_VERSION)

        app_elem = element.find("Application")
        application = Application.from_xml(app_elem) if app_elem is not None else Application()

        transport_elem = element.find("Transport")
        transport = (
            Transport.from_xml(transport_elem) if transport_elem is not None else None
        )

        # Dispatch structure children by tag name
        structure_elem = element.find("Structure")
        structure = []
        if structure_elem is not None:
            for child in structure_elem:
                if child.tag == "Track":
                    structure.append(Track.from_xml(child))
                elif child.tag == "Channel":
                    structure.append(Channel.from_xml(child))
                else:
                    structure.append(Lane.from_xml(child))

        arrangement_elem = element.find("Arrangement")
        arrangement = (
            Arrangement.from_xml(arrangement_elem)
            if arrangement_elem is not None
            else None
        )

        scenes_elem = element.find("Scenes")
        scenes = []
        if scenes_elem is not None:
            for scene_elem in scenes_elem:
                if scene_elem.tag == "Scene":
                    scenes.append(Scene.from_xml(scene_elem))

        return cls(version, application, transport, structure, arrangement, scenes)
