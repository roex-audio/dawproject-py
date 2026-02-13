"""Audio model -- an audio media file on a timeline."""

from .mediaFile import MediaFile
from .timeUnit import TimeUnit


class Audio(MediaFile):
    """An audio file with sample rate, channels, and optional time-stretch algorithm.

    Attributes:
        sample_rate: Sample rate in Hz.
        channels: Number of audio channels.
        algorithm: Optional time-stretch algorithm name.
    """

    def __init__(
        self,
        sample_rate=44100,
        channels=2,
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
        # Default time_unit for Audio is SECONDS
        if self.time_unit is None:
            self.time_unit = TimeUnit.SECONDS

    def to_xml(self):
        elem = super().to_xml()  # MediaFile -> Timeline -> Referenceable -> Nameable
        elem.set("sampleRate", str(self.sample_rate))
        elem.set("channels", str(self.channels))
        if self.algorithm:
            elem.set("algorithm", self.algorithm)
        return elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return None

        instance = super().from_xml(element)  # MediaFile.from_xml handles file, duration, etc.

        instance.sample_rate = int(element.get("sampleRate", 44100))
        instance.channels = int(element.get("channels", 2))
        instance.algorithm = element.get("algorithm")

        # Default time_unit for Audio is SECONDS
        if instance.time_unit is None:
            instance.time_unit = TimeUnit.SECONDS

        return instance
