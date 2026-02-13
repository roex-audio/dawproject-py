"""Note model -- a MIDI note event."""

from lxml import etree as ET
from .doubleAdapter import DoubleAdapter


class Note:
    """A MIDI note with time, duration, pitch, velocity, and optional content.

    It can additionally contain child timelines to hold per-note expression.

    Attributes:
        time: Start time of the note.
        duration: Duration of the note.
        key: MIDI key number.
        channel: MIDI channel (default 0).
        vel: Note-on velocity (normalized).
        rel: Note-off velocity (normalized).
        content: Optional nested Timeline content for per-note expressions.
    """

    def __init__(
        self,
        time=0.0,
        duration=0.0,
        key=0,
        channel=0,
        vel=None,
        rel=None,
        content=None,
    ):
        self.time = time
        self.duration = duration
        self.channel = channel
        self.key = key
        self.vel = vel
        self.rel = rel
        self.content = content

    def to_xml(self):
        note_elem = ET.Element("Note")
        note_elem.set("time", DoubleAdapter.to_xml(self.time))
        note_elem.set("duration", DoubleAdapter.to_xml(self.duration))
        note_elem.set("key", str(self.key))

        if self.channel is not None:
            note_elem.set("channel", str(self.channel))
        if self.vel is not None:
            note_elem.set("vel", DoubleAdapter.to_xml(self.vel))
        if self.rel is not None:
            note_elem.set("rel", DoubleAdapter.to_xml(self.rel))

        # Per-note expression timelines are direct children (no <Content> wrapper)
        if self.content is not None:
            note_elem.append(self.content.to_xml())

        return note_elem

    @classmethod
    def from_xml(cls, element):
        from . import registry

        time = DoubleAdapter.from_xml(element.get("time"))
        duration = DoubleAdapter.from_xml(element.get("duration"))
        key = int(element.get("key"))
        channel = int(element.get("channel")) if element.get("channel") else 0
        vel = (
            DoubleAdapter.from_xml(element.get("vel")) if element.get("vel") else None
        )
        rel = (
            DoubleAdapter.from_xml(element.get("rel")) if element.get("rel") else None
        )

        # Per-note expression: direct Timeline child element (not wrapped in <Content>)
        content = None
        for child in element:
            content_cls = registry.resolve_timeline(child.tag)
            if content_cls is not None:
                content = content_cls.from_xml(child)
                break

        return cls(time, duration, key, channel, vel, rel, content)
