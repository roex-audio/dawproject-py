"""MixerRole enum -- roles for mixer channels."""

from enum import Enum


class MixerRole(Enum):
    """The role of a channel in the mixer."""
    REGULAR = "regular"
    MASTER = "master"
    EFFECT_TRACK = "effect"
    SUB_MIX = "submix"
    VCA = "vca"

    # Aliases for backward compatibility (the short names also work)
    EFFECT = "effect"
    SUBMIX = "submix"
