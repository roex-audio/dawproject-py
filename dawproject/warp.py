"""Warp model -- a time-warp point mapping timeline time to content time."""

from lxml import etree as ET


class Warp:
    """A single warp point mapping a timeline position to a content position.

    Attributes:
        time: Position in the timeline.
        content_time: Corresponding position in the content.
    """

    def __init__(self, time=0.0, content_time=0.0):
        self.time = time
        self.content_time = content_time

    def to_xml(self):
        warp_elem = ET.Element("Warp")
        warp_elem.set("time", str(self.time))
        warp_elem.set("contentTime", str(self.content_time))
        return warp_elem

    @classmethod
    def from_xml(cls, element):
        time = float(element.get("time", 0.0))
        content_time = float(element.get("contentTime", 0.0))
        return cls(time, content_time)
