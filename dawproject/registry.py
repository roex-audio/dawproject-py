"""Central type registry mapping XML tag names to Python classes.

This replaces the broken globals()-based lookup pattern that was used
for polymorphic deserialization across modules.
"""

# Registry dict: XML tag name -> class
_TAG_REGISTRY = {}


def register(tag_name, cls):
    """Register a class for a given XML tag name."""
    _TAG_REGISTRY[tag_name] = cls


def get_class(tag_name):
    """Look up a class by XML tag name. Returns None if not found."""
    return _TAG_REGISTRY.get(tag_name)


def populate_registry():
    """Populate the registry with all known DAWproject types.

    This is called lazily on first use to avoid circular import issues.
    """
    if _TAG_REGISTRY:
        return  # Already populated

    from .lanes import Lanes
    from .clips import Clips
    from .notes import Notes
    from .markers import Markers
    from .points import Points
    from .warps import Warps
    from .audio import Audio
    from .video import Video
    from .mediaFile import MediaFile
    from .clipSlot import ClipSlot
    from .realPoint import RealPoint
    from .boolPoint import BoolPoint
    from .enumPoint import EnumPoint
    from .integerPoint import IntegerPoint
    from .timeSignaturePoint import TimeSignaturePoint
    from .boolParameter import BoolParameter
    from .realParameter import RealParameter
    from .integerParameter import IntegerParameter
    from .enumParameter import EnumParameter
    from .device import Device
    from .builtInDevice import BuiltInDevice
    from .equalizer import Equalizer
    from .compressor import Compressor
    from .noiseGate import NoiseGate
    from .limiter import Limiter
    from .plugin import Plugin
    from .vst2Plugin import Vst2Plugin
    from .vst3Plugin import Vst3Plugin
    from .clapPlugin import ClapPlugin
    from .auPlugin import AuPlugin

    # Timeline subclasses
    register("Lanes", Lanes)
    register("Clips", Clips)
    register("Notes", Notes)
    register("Markers", Markers)
    register("markers", Markers)  # XSD global element is lowercase
    register("Points", Points)
    register("Warps", Warps)
    register("Audio", Audio)
    register("Video", Video)
    register("MediaFile", MediaFile)
    register("ClipSlot", ClipSlot)

    # Point subclasses
    register("RealPoint", RealPoint)
    register("BoolPoint", BoolPoint)
    register("EnumPoint", EnumPoint)
    register("IntegerPoint", IntegerPoint)
    register("TimeSignaturePoint", TimeSignaturePoint)

    # Parameter subclasses
    register("BoolParameter", BoolParameter)
    register("RealParameter", RealParameter)
    register("IntegerParameter", IntegerParameter)
    register("EnumParameter", EnumParameter)

    # Device subclasses
    register("Device", Device)
    register("BuiltinDevice", BuiltInDevice)
    register("Equalizer", Equalizer)
    register("Compressor", Compressor)
    register("NoiseGate", NoiseGate)
    register("Limiter", Limiter)
    register("Plugin", Plugin)
    register("Vst2Plugin", Vst2Plugin)
    register("Vst3Plugin", Vst3Plugin)
    register("ClapPlugin", ClapPlugin)
    register("AuPlugin", AuPlugin)


def resolve_timeline(tag_name):
    """Look up a Timeline subclass by XML tag name."""
    populate_registry()
    return get_class(tag_name)


def resolve_point(tag_name):
    """Look up a Point subclass by XML tag name."""
    populate_registry()
    return get_class(tag_name)


def resolve_parameter(tag_name):
    """Look up a Parameter subclass by XML tag name."""
    populate_registry()
    return get_class(tag_name)


def resolve_device(tag_name):
    """Look up a Device subclass by XML tag name."""
    populate_registry()
    return get_class(tag_name)
