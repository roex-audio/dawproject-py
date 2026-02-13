"""Nameable model -- base class for objects with name, color, and comment."""

from abc import ABC
from lxml import etree as ET


class Nameable(ABC):
    """Abstract base class for objects with name, color, and comment attributes.

    Attributes:
        name: Display name.
        color: Color string (e.g. hex color).
        comment: Optional comment text.
    """

    def __init__(self, name=None, color=None, comment=None):
        self.name = name
        self.color = color
        self.comment = comment

    def to_xml(self):
        element = ET.Element(self.__class__.__name__)

        if self.name is not None:
            element.set("name", self.name)
        if self.color is not None:
            element.set("color", self.color)
        if self.comment is not None:
            element.set("comment", self.comment)

        return element

    @classmethod
    def from_xml(cls, element):
        """Create an instance from an XML element.

        Uses __new__ to avoid positional arg mismatch in subclass constructors,
        then sets name/color/comment from element attributes.
        """
        instance = cls.__new__(cls)
        # Initialize all __init__ defaults to avoid missing attributes
        instance.name = element.get("name") if element is not None else None
        instance.color = element.get("color") if element is not None else None
        instance.comment = element.get("comment") if element is not None else None
        return instance
