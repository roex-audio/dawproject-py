"""Clips model -- a container for Clip objects on a timeline."""

from .timeline import Timeline
from .clip import Clip


class Clips(Timeline):
    """A timeline containing a sequence of clips.

    Attributes:
        clips: List of Clip objects.
    """

    def __init__(
        self,
        clips=None,
        track=None,
        time_unit=None,
        name=None,
        color=None,
        comment=None,
    ):
        super().__init__(track, time_unit, name, color, comment)
        self.clips = clips if clips else []

    def to_xml(self):
        elem = super().to_xml()
        for clip in self.clips:
            elem.append(clip.to_xml())
        return elem

    @classmethod
    def from_xml(cls, element):
        instance = super().from_xml(element)

        clips = []
        for clip_elem in element.findall("Clip"):
            clips.append(Clip.from_xml(clip_elem))
        instance.clips = clips

        return instance
