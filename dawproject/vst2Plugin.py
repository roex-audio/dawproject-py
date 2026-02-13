"""Vst2Plugin model -- a VST2 plug-in instance."""

from .plugin import Plugin


class Vst2Plugin(Plugin):
    """A VST2 Plug-in instance.

    The VST2 plug-in state should be stored in FXB or FXP format.
    """
    pass
