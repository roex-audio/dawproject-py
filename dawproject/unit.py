"""Unit enum -- measurement units for parameters."""

from enum import Enum


class Unit(Enum):
    """Units of measurement for parameter values."""
    LINEAR = "linear"
    NORMALIZED = "normalized"
    PERCENT = "percent"
    DECIBEL = "decibel"
    HERTZ = "hertz"
    SEMITONES = "semitones"
    SECONDS = "seconds"
    BEATS = "beats"
    BPM = "bpm"
