"""Marker model -- a named marker on a timeline."""

from .nameable import Nameable


class Marker(Nameable):
    """A named marker at a specific time position.

    Attributes:
        time: The time position of the marker.
    """

    def __init__(self, time=0.0, name=None, color=None, comment=None):
        super().__init__(name, color, comment)
        self.time = time

    def to_xml(self):
        marker_elem = super().to_xml()
        marker_elem.tag = "Marker"
        marker_elem.set("time", str(self.time))
        return marker_elem

    @classmethod
    def from_xml(cls, element):
        instance = super().from_xml(element)
        time = element.get("time")
        instance.time = float(time) if time is not None else 0.0
        return instance
