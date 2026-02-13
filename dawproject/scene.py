"""Scene model -- a scene containing timeline content."""

from lxml import etree as ET
from .referenceable import Referenceable


class Scene(Referenceable):
    """A scene that holds a Timeline content object.

    Attributes:
        content: A Timeline subclass instance.
    """

    def __init__(self, content=None, name=None, color=None, comment=None):
        super().__init__(name, color, comment)
        self.content = content

    def to_xml(self):
        scene_elem = super().to_xml()
        scene_elem.tag = "Scene"

        if self.content is not None:
            scene_elem.append(self.content.to_xml())

        return scene_elem

    @classmethod
    def from_xml(cls, element):
        from . import registry

        instance = super().from_xml(element)

        # Look for a Timeline subclass child element
        instance.content = None
        for child in element:
            content_cls = registry.resolve_timeline(child.tag)
            if content_cls is not None:
                instance.content = content_cls.from_xml(child)
                break

        return instance
