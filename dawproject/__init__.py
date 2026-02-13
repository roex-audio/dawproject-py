"""
dawproject - Python library for working with DAWProject files.

A Python port of the Java DAWProject library by Bitwig, enabling
seamless project exchange between DAWs using the open XML-based
DAWProject format.
"""

# Main entry point
from .dawProject import DawProject

# Project model
from .project import Project
from .application import Application
from .metaData import MetaData
from .transport import Transport

# Structure
from .track import Track
from .channel import Channel
from .lane import Lane
from .arrangement import Arrangement
from .scene import Scene
from .send import Send

# Timeline types
from .timeline import Timeline
from .lanes import Lanes
from .clips import Clips
from .clip import Clip
from .clipSlot import ClipSlot
from .notes import Notes
from .note import Note
from .markers import Markers
from .marker import Marker
from .points import Points
from .warps import Warps
from .warp import Warp
from .audio import Audio
from .video import Video
from .mediaFile import MediaFile

# Parameters
from .realParameter import RealParameter
from .boolParameter import BoolParameter
from .integerParameter import IntegerParameter
from .enumParameter import EnumParameter
from .parameter import Parameter
from .timeSignatureParameter import TimeSignatureParameter
from .automationTarget import AutomationTarget

# Devices
from .device import Device
from .builtInDevice import BuiltinDevice, BuiltInDevice  # BuiltInDevice kept as alias
from .plugin import Plugin
from .vst2Plugin import Vst2Plugin
from .vst3Plugin import Vst3Plugin
from .clapPlugin import ClapPlugin
from .auPlugin import AuPlugin
from .equalizer import Equalizer
from .compressor import Compressor
from .noiseGate import NoiseGate
from .limiter import Limiter
from .eqBand import EqBand

# Enums
from .contentType import ContentType
from .mixerRole import MixerRole
from .timeUnit import TimeUnit
from .unit import Unit
from .interpolation import Interpolation
from .sendType import SendType
from .deviceRole import DeviceRole
from .eqBandType import EqBandType
from .expressionType import ExpressionType

# Helpers
from .utility import Utility
from .referenceable import Referenceable
from .nameable import Nameable
from .fileReference import FileReference
from .doubleAdapter import DoubleAdapter
from .realPoint import RealPoint
from .boolPoint import BoolPoint
from .enumPoint import EnumPoint
from .integerPoint import IntegerPoint
from .timeSignaturePoint import TimeSignaturePoint
from .point import Point

__all__ = [
    # Main
    "DawProject",
    # Project model
    "Project",
    "Application",
    "MetaData",
    "Transport",
    # Structure
    "Track",
    "Channel",
    "Lane",
    "Arrangement",
    "Scene",
    "Send",
    # Timeline
    "Timeline",
    "Lanes",
    "Clips",
    "Clip",
    "ClipSlot",
    "Notes",
    "Note",
    "Markers",
    "Marker",
    "Points",
    "Warps",
    "Warp",
    "Audio",
    "Video",
    "MediaFile",
    # Parameters
    "RealParameter",
    "BoolParameter",
    "IntegerParameter",
    "EnumParameter",
    "Parameter",
    "TimeSignatureParameter",
    "AutomationTarget",
    # Devices
    "Device",
    "BuiltinDevice",
    "BuiltInDevice",  # backward-compatible alias
    "Plugin",
    "Vst2Plugin",
    "Vst3Plugin",
    "ClapPlugin",
    "AuPlugin",
    "Equalizer",
    "Compressor",
    "NoiseGate",
    "Limiter",
    "EqBand",
    # Enums
    "ContentType",
    "MixerRole",
    "TimeUnit",
    "Unit",
    "Interpolation",
    "SendType",
    "DeviceRole",
    "EqBandType",
    "ExpressionType",
    # Helpers
    "Utility",
    "Referenceable",
    "Nameable",
    "FileReference",
    "DoubleAdapter",
    "RealPoint",
    "BoolPoint",
    "EnumPoint",
    "IntegerPoint",
    "TimeSignaturePoint",
    "Point",
]
