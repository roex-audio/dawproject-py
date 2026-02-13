"""Clip model -- a clip on a timeline."""

from lxml import etree as ET
from .nameable import Nameable
from .referenceable import Referenceable
from .timeUnit import TimeUnit
from .doubleAdapter import DoubleAdapter


class Clip(Nameable):
    """A clip wrapping some timeline content with position and duration.

    Attributes:
        time: Start time of the clip.
        duration: Duration of the clip.
        content_time_unit: TimeUnit for content positioning.
        play_start: Start point for playback within content.
        play_stop: Stop point for playback within content.
        loop_start: Loop start point.
        loop_end: Loop end point.
        fade_time_unit: TimeUnit for fade times.
        fade_in_time: Fade-in duration.
        fade_out_time: Fade-out duration.
        content: A Timeline object (Audio, Notes, etc.).
        reference: A Referenceable reference.
    """

    def __init__(
        self,
        time=0.0,
        duration=None,
        content_time_unit=None,
        play_start=None,
        play_stop=None,
        loop_start=None,
        loop_end=None,
        fade_time_unit=None,
        fade_in_time=None,
        fade_out_time=None,
        content=None,
        reference=None,
        name=None,
        color=None,
        comment=None,
    ):
        super().__init__(name, color, comment)
        self.time = time
        self.duration = duration
        self.content_time_unit = content_time_unit
        self.play_start = play_start
        self.play_stop = play_stop
        self.loop_start = loop_start
        self.loop_end = loop_end
        self.fade_time_unit = fade_time_unit
        self.fade_in_time = fade_in_time
        self.fade_out_time = fade_out_time
        self.content = content
        self.reference = reference

    def to_xml(self):
        clip_elem = ET.Element("Clip")

        clip_elem.set("time", DoubleAdapter.to_xml(self.time))
        if self.duration is not None:
            clip_elem.set("duration", DoubleAdapter.to_xml(self.duration))
        if self.content_time_unit is not None:
            clip_elem.set("contentTimeUnit", self.content_time_unit.value)
        if self.play_start is not None:
            clip_elem.set("playStart", DoubleAdapter.to_xml(self.play_start))
        if self.play_stop is not None:
            clip_elem.set("playStop", DoubleAdapter.to_xml(self.play_stop))
        if self.loop_start is not None:
            clip_elem.set("loopStart", DoubleAdapter.to_xml(self.loop_start))
        if self.loop_end is not None:
            clip_elem.set("loopEnd", DoubleAdapter.to_xml(self.loop_end))
        if self.fade_time_unit is not None:
            clip_elem.set("fadeTimeUnit", self.fade_time_unit.value)
        if self.fade_in_time is not None:
            clip_elem.set("fadeInTime", DoubleAdapter.to_xml(self.fade_in_time))
        if self.fade_out_time is not None:
            clip_elem.set("fadeOutTime", DoubleAdapter.to_xml(self.fade_out_time))

        if self.content is not None:
            clip_elem.append(self.content.to_xml())

        if self.reference is not None:
            clip_elem.set("reference", self.reference.id)

        # Append inherited attributes (name, color, comment)
        nameable_elem = super().to_xml()
        for key, value in nameable_elem.attrib.items():
            clip_elem.set(key, value)

        return clip_elem

    @classmethod
    def from_xml(cls, element):
        from . import registry

        instance = super().from_xml(element)

        parsed_time = DoubleAdapter.from_xml(element.get("time"))
        instance.time = parsed_time if parsed_time is not None else 0.0
        instance.duration = DoubleAdapter.from_xml(element.get("duration"))

        ctu = element.get("contentTimeUnit")
        try:
            instance.content_time_unit = TimeUnit(ctu) if ctu else None
        except ValueError:
            instance.content_time_unit = None

        instance.play_start = DoubleAdapter.from_xml(element.get("playStart"))
        instance.play_stop = DoubleAdapter.from_xml(element.get("playStop"))
        instance.loop_start = DoubleAdapter.from_xml(element.get("loopStart"))
        instance.loop_end = DoubleAdapter.from_xml(element.get("loopEnd"))

        ftu = element.get("fadeTimeUnit")
        try:
            instance.fade_time_unit = TimeUnit(ftu) if ftu else None
        except ValueError:
            instance.fade_time_unit = None

        instance.fade_in_time = DoubleAdapter.from_xml(element.get("fadeInTime"))
        instance.fade_out_time = DoubleAdapter.from_xml(element.get("fadeOutTime"))

        # Look for content as any known Timeline subclass child element
        instance.content = None
        for child in element:
            content_cls = registry.resolve_timeline(child.tag)
            if content_cls is not None:
                instance.content = content_cls.from_xml(child)
                break

        reference_id = element.get("reference")
        if reference_id:
            instance.reference = Referenceable.get_by_id(reference_id)
        else:
            instance.reference = None

        return instance
