"""Video model -- a video media file on a timeline."""

from .mediaFile import MediaFile
from .timeUnit import TimeUnit


class Video(MediaFile):
    """A video file with optional audio properties and time-stretch algorithm.

    Duration should be the entire length of the file; any clipping should be
    done by placing the Video element within a Clip element. The timeUnit
    attribute should always be set to seconds.

    Attributes:
        sample_rate: Sample rate of audio in Hz (if present).
        channels: Number of audio channels (1=mono, if present).
        algorithm: Playback algorithm used to warp audio (vendor-specific, if present).
    """

    def __init__(
        self,
        sample_rate=0,
        channels=0,
        duration=0.0,
        algorithm=None,
        file=None,
        name=None,
        time_unit=None,
        **kwargs,
    ):
        super().__init__(file=file, duration=duration, name=name, time_unit=time_unit, **kwargs)
        self.sample_rate = sample_rate
        self.channels = channels
        self.algorithm = algorithm
        if self.time_unit is None:
            self.time_unit = TimeUnit.SECONDS

    def to_xml(self):
        elem = super().to_xml()
        if self.sample_rate:
            elem.set("sampleRate", str(self.sample_rate))
        if self.channels:
            elem.set("channels", str(self.channels))
        if self.algorithm:
            elem.set("algorithm", self.algorithm)
        return elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return None

        instance = super().from_xml(element)

        sample_rate = element.get("sampleRate")
        instance.sample_rate = int(sample_rate) if sample_rate else 0
        channels = element.get("channels")
        instance.channels = int(channels) if channels else 0
        instance.algorithm = element.get("algorithm")

        if instance.time_unit is None:
            instance.time_unit = TimeUnit.SECONDS

        return instance
