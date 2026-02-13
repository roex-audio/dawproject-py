"""Plugin model -- abstract base class for all plug-in formats."""

from .device import Device


class Plugin(Device):
    """Abstract base class for all plug-in formats (VST2, VST3, CLAP, AU).

    Attributes:
        plugin_version: Version string of the plug-in.
    """

    def __init__(self, plugin_version=None, **kwargs):
        super().__init__(**kwargs)
        self.plugin_version = plugin_version

    def to_xml(self):
        elem = super().to_xml()
        if self.plugin_version is not None:
            elem.set("pluginVersion", self.plugin_version)
        return elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return None
        instance = super().from_xml(element)
        instance.plugin_version = element.get("pluginVersion")
        return instance
