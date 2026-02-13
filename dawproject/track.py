"""Track model -- a track in the project structure."""

from lxml import etree as ET
from .lane import Lane
from .channel import Channel
from .contentType import ContentType


class Track(Lane):
    """A track within the project structure, containing a channel and optional nested tracks.

    Attributes:
        content_type: A set/list of ContentType values indicating what this track contains.
        loaded: Boolean indicating whether the track is loaded.
        channel: The Channel associated with this track.
        tracks: Nested child Track objects.
    """

    def __init__(
        self,
        content_type=None,
        loaded=None,
        channel=None,
        tracks=None,
        name=None,
        color=None,
        comment=None,
    ):
        super().__init__(name, color, comment)
        self.content_type = content_type if content_type else []
        self.loaded = loaded
        self.channel = channel
        self.tracks = tracks if tracks else []

    def to_xml(self):
        track_elem = super().to_xml()
        track_elem.tag = "Track"

        # Set content_type as a space-separated attribute (per XSD xs:list)
        if self.content_type:
            content_type_str = " ".join(
                ct.value if isinstance(ct, ContentType) else str(ct)
                for ct in self.content_type
            )
            track_elem.set("contentType", content_type_str)

        if self.loaded is not None:
            track_elem.set("loaded", str(self.loaded).lower())

        # Append Channel as a nested XML element
        if self.channel is not None:
            track_elem.append(self.channel.to_xml())

        # Recursively add nested tracks
        for track in self.tracks:
            track_elem.append(track.to_xml())

        return track_elem

    @classmethod
    def from_xml(cls, element):
        instance = super().from_xml(element)

        # Read contentType as a space-separated XML attribute (per XSD xs:list).
        # Also accept commas for backward compatibility with older files.
        content_type_str = element.get("contentType")
        if content_type_str:
            # Normalize: replace commas with spaces, then split on whitespace
            normalized = content_type_str.replace(",", " ")
            instance.content_type = [
                ContentType(ct) for ct in normalized.split() if ct
            ]
        else:
            instance.content_type = []

        loaded = element.get("loaded")
        instance.loaded = loaded.lower() == "true" if loaded else None

        channel_elem = element.find("Channel")
        instance.channel = (
            Channel.from_xml(channel_elem) if channel_elem is not None else None
        )

        tracks = []
        for track_elem in element.findall("Track"):
            tracks.append(Track.from_xml(track_elem))
        instance.tracks = tracks

        return instance
