"""Lanes model -- a container of Timeline elements."""

from .timeline import Timeline


class Lanes(Timeline):
    """A container for multiple Timeline elements (Clips, Notes, Points, etc.).

    Attributes:
        lanes: List of Timeline objects contained in this Lanes.
    """

    def __init__(
        self,
        lanes=None,
        track=None,
        time_unit=None,
        name=None,
        color=None,
        comment=None,
    ):
        super().__init__(track, time_unit, name, color, comment)
        self.lanes = lanes if lanes else []

    def to_xml(self):
        elem = super().to_xml()
        for lane in self.lanes:
            elem.append(lane.to_xml())
        return elem

    @classmethod
    def from_xml(cls, element):
        from . import registry

        instance = super().from_xml(element)

        # Resolve child elements as Timeline subclasses via registry
        lanes = []
        for child in element:
            child_cls = registry.resolve_timeline(child.tag)
            if child_cls is not None:
                lanes.append(child_cls.from_xml(child))
        instance.lanes = lanes

        return instance
