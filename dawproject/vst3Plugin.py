"""Vst3Plugin model -- a VST3 plug-in instance."""

from .plugin import Plugin


class Vst3Plugin(Plugin):
    """A VST3 Plug-in instance.

    The VST3 plug-in state should be stored in .vstpreset format.
    """
    pass
