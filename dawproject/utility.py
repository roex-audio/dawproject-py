"""Utility class -- factory methods for creating common DAWproject objects."""

from typing import Set

from .track import Track
from .channel import Channel
from .realParameter import RealParameter
from .audio import Audio
from .fileReference import FileReference
from .warp import Warp
from .clip import Clip
from .clips import Clips
from .timeUnit import TimeUnit
from .contentType import ContentType
from .mixerRole import MixerRole
from .unit import Unit
from .timeline import Timeline


class Utility:
    """Convenience factory for building common DAWproject objects."""

    @staticmethod
    def create_track(
        name: str,
        content_types: Set[ContentType],
        mixer_role: MixerRole,
        volume: float,
        pan: float,
    ) -> Track:
        """Create a Track with an associated Channel.

        Args:
            name: Track name.
            content_types: Set of ContentType values for the track.
            mixer_role: MixerRole enum for the channel.
            volume: Volume level (linear, 0.0-1.0).
            pan: Pan position (normalized, 0.0-1.0).

        Returns:
            A new Track instance.
        """
        track_channel = Channel(
            volume=RealParameter(value=volume, unit=Unit.LINEAR),
            pan=RealParameter(value=pan, unit=Unit.NORMALIZED),
            role=mixer_role,
        )
        track = Track(
            name=name,
            channel=track_channel,
            content_type=content_types,
            loaded=True,
        )
        return track

    @staticmethod
    def create_audio(
        relative_path: str, sample_rate: int, channels: int, duration: float
    ) -> Audio:
        """Create an Audio timeline element.

        Args:
            relative_path: Path to the audio file.
            sample_rate: Sample rate in Hz.
            channels: Number of audio channels.
            duration: Duration in seconds.

        Returns:
            A new Audio instance.
        """
        audio = Audio(
            time_unit=TimeUnit.SECONDS,
            file=FileReference(path=relative_path, external=False),
            sample_rate=sample_rate,
            channels=channels,
            duration=duration,
        )
        return audio

    @staticmethod
    def create_warp(time: float, content_time: float) -> Warp:
        """Create a Warp point.

        Args:
            time: Time position in the timeline.
            content_time: Time position in the content.

        Returns:
            A new Warp instance.
        """
        return Warp(time=time, content_time=content_time)

    @staticmethod
    def create_clip(content: Timeline, time: float, duration: float) -> Clip:
        """Create a Clip wrapping some timeline content.

        Args:
            content: The Timeline content (Audio, Notes, etc.).
            time: Start time of the clip.
            duration: Duration of the clip.

        Returns:
            A new Clip instance.
        """
        return Clip(content=content, time=time, duration=duration)

    @staticmethod
    def create_clips(*clips: Clip) -> Clips:
        """Create a Clips timeline container from one or more clips.

        Args:
            *clips: Clip instances to include.

        Returns:
            A new Clips instance.
        """
        return Clips(clips=list(clips))
