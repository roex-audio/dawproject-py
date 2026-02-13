"""Point model -- abstract base for automation points."""

from abc import ABC
from lxml import etree as ET
from .doubleAdapter import DoubleAdapter


class Point(ABC):
    """Abstract base class for automation points.

    Attributes:
        time: The time position of this point.
    """

    def __init__(self, time=None):
        self.time = time

    def to_xml(self):
        point_elem = ET.Element(self.__class__.__name__)
        if self.time is not None:
            point_elem.set("time", DoubleAdapter.to_xml(self.time))
        return point_elem

    @classmethod
    def from_xml(cls, element):
        instance = cls.__new__(cls)
        time = element.get("time")
        instance.time = DoubleAdapter.from_xml(time) if time is not None else None
        return instance
