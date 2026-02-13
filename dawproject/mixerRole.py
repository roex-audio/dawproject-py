"""MixerRole enum -- roles for mixer channels."""

from enum import Enum


class MixerRole(Enum):
    """The role of a channel in the mixer."""
    REGULAR = "regular"
    MASTER = "master"
    EFFECT = "effect"
    SUBMIX = "submix"
    VCA = "vca"
