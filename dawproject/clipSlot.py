"""ClipSlot model -- a clip launcher slot within a Scene."""

from .timeline import Timeline
from .clip import Clip


class ClipSlot(Timeline):
    """A clip launcher slot within a Scene that can contain a Clip.

    It is generally set to a specific track.

    Attributes:
        has_stop: Whether launching this slot should stop track playback when empty.
        clip: The contained Clip, if any.
    """

    def __init__(self, has_stop=None, clip=None, **kwargs):
        super().__init__(**kwargs)
        self.has_stop = has_stop
        self.clip = clip

    def to_xml(self):
        elem = super().to_xml()
        if self.has_stop is not None:
            elem.set("hasStop", str(self.has_stop).lower())
        if self.clip is not None:
            elem.append(self.clip.to_xml())
        return elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return None

        instance = super().from_xml(element)

        has_stop = element.get("hasStop")
        instance.has_stop = has_stop.lower() == "true" if has_stop is not None else None

        clip_elem = element.find("Clip")
        instance.clip = Clip.from_xml(clip_elem) if clip_elem is not None else None

        return instance
