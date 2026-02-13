"""Timeline model -- abstract base for all timeline content types."""

from .referenceable import Referenceable


class Timeline(Referenceable):
    """Abstract base class for timeline content types (Lanes, Clips, Notes, etc.).

    Attributes:
        track: Reference to the Track this timeline belongs to.
        time_unit: TimeUnit for this timeline.
    """

    def __init__(self, track=None, time_unit=None, name=None, color=None, comment=None):
        super().__init__(name, color, comment)
        self.track = track
        self.time_unit = time_unit

    def to_xml(self):
        """Serialize base Timeline attributes (id, name, color, comment, track, timeUnit)."""
        from .timeUnit import TimeUnit

        elem = super().to_xml()  # Referenceable adds id; Nameable adds name/color/comment
        if self.track is not None:
            elem.set("track", str(self.track.id))
        if self.time_unit is not None:
            tu = self.time_unit.value if isinstance(self.time_unit, TimeUnit) else str(self.time_unit)
            elem.set("timeUnit", tu)
        return elem

    @classmethod
    def from_xml(cls, element):
        """Base deserialization for Timeline attributes."""
        instance = super().from_xml(element)

        # Parse track reference
        track_id = element.get("track")
        if track_id:
            instance.track = Referenceable.get_by_id(track_id)
        else:
            instance.track = None

        # Parse time_unit
        time_unit_str = element.get("timeUnit")
        if time_unit_str:
            from .timeUnit import TimeUnit
            try:
                instance.time_unit = TimeUnit(time_unit_str)
            except ValueError:
                instance.time_unit = None
        else:
            instance.time_unit = None

        return instance
