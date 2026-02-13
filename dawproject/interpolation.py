"""Interpolation enum -- interpolation modes for automation points."""

from enum import Enum


class Interpolation(Enum):
    """Interpolation mode between automation points."""
    HOLD = "hold"
    LINEAR = "linear"
