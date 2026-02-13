"""SendType enum -- pre/post send types."""

from enum import Enum


class SendType(Enum):
    """Whether a send is pre-fader or post-fader."""
    PRE = "pre"
    POST = "post"
