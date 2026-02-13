"""Warps model -- time-warped content."""

from .timeline import Timeline
from .warp import Warp
from .timeUnit import TimeUnit


class Warps(Timeline):
    """A warped timeline containing warp points and nested content.

    Attributes:
        events: List of Warp points.
        content: A nested Timeline (Audio, etc.) being warped.
        content_time_unit: The TimeUnit for content time.
    """

    def __init__(self, events=None, content=None, content_time_unit=None, **kwargs):
        super().__init__(**kwargs)
        self.events = events if events is not None else []
        self.content = content
        self.content_time_unit = content_time_unit

    def to_xml(self):
        elem = super().to_xml()
        if self.content_time_unit is not None:
            elem.set("contentTimeUnit", self.content_time_unit.value)
        if self.content is not None:
            elem.append(self.content.to_xml())
        for warp in self.events:
            elem.append(warp.to_xml())
        return elem

    @classmethod
    def from_xml(cls, element):
        from . import registry

        instance = super().from_xml(element)

        # Parse content -- find first Timeline subclass child (not Warp)
        content = None
        for child in element:
            if child.tag != "Warp":
                content_cls = registry.resolve_timeline(child.tag)
                if content_cls is not None:
                    content = content_cls.from_xml(child)
                    break
        instance.content = content

        events = []
        for warp_elem in element.findall("Warp"):
            events.append(Warp.from_xml(warp_elem))
        instance.events = events

        content_time_unit_str = element.get("contentTimeUnit")
        try:
            instance.content_time_unit = TimeUnit(content_time_unit_str) if content_time_unit_str else None
        except ValueError:
            instance.content_time_unit = None

        return instance
