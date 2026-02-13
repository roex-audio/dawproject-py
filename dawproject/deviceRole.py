"""DeviceRole enum -- roles for audio devices."""

from enum import Enum


class DeviceRole(Enum):
    """The role of a device in a channel's processing chain."""
    INSTRUMENT = "instrument"
    NOTE_FX = "noteFX"
    AUDIO_FX = "audioFX"
    ANALYZER = "analyzer"
