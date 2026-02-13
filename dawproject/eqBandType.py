"""EqBandType enum -- types of EQ filter bands."""

from enum import Enum


class EqBandType(Enum):
    """The type of an EQ filter band."""
    HIGH_PASS = "highPass"
    LOW_PASS = "lowPass"
    BAND_PASS = "bandPass"
    HIGH_SHELF = "highShelf"
    LOW_SHELF = "lowShelf"
    BELL = "bell"
    NOTCH = "notch"
