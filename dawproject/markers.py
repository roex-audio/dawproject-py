"""Markers model -- a container for Marker objects on a timeline."""

from .timeline import Timeline
from .marker import Marker


class Markers(Timeline):
    """A timeline containing markers.

    Attributes:
        markers: List of Marker objects.
    """

    def __init__(
        self,
        markers=None,
        track=None,
        time_unit=None,
        name=None,
        color=None,
        comment=None,
    ):
        super().__init__(track, time_unit, name, color, comment)
        self.markers = markers if markers else []

    def to_xml(self):
        elem = super().to_xml()
        for marker in self.markers:
            elem.append(marker.to_xml())
        return elem

    @classmethod
    def from_xml(cls, element):
        instance = super().from_xml(element)

        markers = []
        for marker_elem in element.findall("Marker"):
            markers.append(Marker.from_xml(marker_elem))
        instance.markers = markers

        return instance
