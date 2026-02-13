"""ExpressionType enum -- expression types for automation targets."""

from enum import Enum


class ExpressionType(Enum):
    """Types of expression for automation and modulation."""
    GAIN = "gain"
    PAN = "pan"
    TRANSPOSE = "transpose"
    TIMBRE = "timbre"
    FORMANT = "formant"
    PRESSURE = "pressure"
    CHANNEL_CONTROLLER = "channelController"
    CHANNEL_PRESSURE = "channelPressure"
    POLY_PRESSURE = "polyPressure"
    PITCH_BEND = "pitchBend"
    PROGRAM_CHANGE = "programChange"
