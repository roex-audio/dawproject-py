"""MediaFile model -- a timeline element representing a media file."""

from .fileReference import FileReference
from .timeline import Timeline
from .doubleAdapter import DoubleAdapter


class MediaFile(Timeline):
    """A media file reference with duration, used as base for Audio, Video, etc.

    Attributes:
        file: A FileReference to the media file.
        duration: Duration in seconds.
    """

    def __init__(self, file=None, duration=0.0, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.file = file if file else FileReference(path="")
        self.duration = duration

    def to_xml(self):
        elem = super().to_xml()
        elem.set("duration", DoubleAdapter.to_xml(self.duration))
        file_elem = self.file.to_xml()
        file_elem.tag = "File"
        elem.append(file_elem)
        return elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return None

        instance = super().from_xml(element)

        file_elem = element.find("File")
        instance.file = (
            FileReference.from_xml(file_elem)
            if file_elem is not None
            else FileReference(path="")
        )
        instance.duration = DoubleAdapter.from_xml(element.get("duration")) or 0.0

        return instance
