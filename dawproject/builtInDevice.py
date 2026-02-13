"""BuiltinDevice model -- base class for built-in devices (Equalizer, Compressor, etc.)."""

from .device import Device


class BuiltinDevice(Device):
    """Base class for built-in audio devices such as Equalizer, Compressor, NoiseGate, or Limiter.

    This is a pass-through in the class hierarchy (matching the XSD where
    builtinDevice is an empty extension of device). Concrete devices like
    Equalizer and Compressor extend this class and add their own elements.
    """
    pass


# Backward-compatible alias
BuiltInDevice = BuiltinDevice
