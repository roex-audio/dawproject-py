"""ContentType enum -- types of content a track can contain."""

from enum import Enum


class ContentType(Enum):
    """The type of content in a track."""
    AUDIO = "audio"
    AUTOMATION = "automation"
    NOTES = "notes"
    VIDEO = "video"
    MARKERS = "markers"
    TRACKS = "tracks"
