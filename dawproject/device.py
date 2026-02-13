"""Device model -- a generic device in a channel's device chain."""

from lxml import etree as ET
from .referenceable import Referenceable
from .boolParameter import BoolParameter
from .deviceRole import DeviceRole
from .fileReference import FileReference


class Device(Referenceable):
    """A device (plugin, built-in effect, etc.) within a Channel.

    Attributes:
        enabled: BoolParameter for enabled state.
        device_role: DeviceRole enum.
        loaded: Boolean indicating if the device is loaded.
        device_name: Display name of the device.
        device_id: Unique device identifier.
        device_vendor: Device vendor name.
        state: FileReference for device state.
        automated_parameters: List of automated Parameter objects.
    """

    def __init__(
        self,
        enabled=None,
        device_role=None,
        loaded=True,
        device_name=None,
        device_id=None,
        device_vendor=None,
        state=None,
        automated_parameters=None,
        name=None,
        color=None,
        comment=None,
    ):
        super().__init__(name, color, comment)
        self.enabled = enabled
        self.device_role = device_role
        self.loaded = loaded
        self.device_name = device_name
        self.device_id = device_id
        self.device_vendor = device_vendor
        self.state = state
        self.automated_parameters = automated_parameters if automated_parameters else []

    def to_xml(self):
        device_elem = super().to_xml()

        if self.automated_parameters:
            parameters_elem = ET.SubElement(device_elem, "Parameters")
            for param in self.automated_parameters:
                parameters_elem.append(param.to_xml())

        if self.enabled is not None:
            enabled_xml = self.enabled.to_xml()
            enabled_xml.tag = "Enabled"
            device_elem.append(enabled_xml)

        if self.device_role is not None:
            role_val = self.device_role.value if isinstance(self.device_role, DeviceRole) else str(self.device_role)
            device_elem.set("deviceRole", role_val)

        if self.loaded is not None:
            device_elem.set("loaded", str(self.loaded).lower())

        if self.device_name is not None:
            device_elem.set("deviceName", self.device_name)

        if self.device_id is not None:
            device_elem.set("deviceID", self.device_id)

        if self.device_vendor is not None:
            device_elem.set("deviceVendor", self.device_vendor)

        if self.state is not None:
            state_xml = self.state.to_xml()
            state_xml.tag = "State"
            device_elem.append(state_xml)

        return device_elem

    @classmethod
    def from_xml(cls, element):
        from . import registry

        instance = super().from_xml(element)

        enabled_elem = element.find("Enabled")
        instance.enabled = (
            BoolParameter.from_xml(enabled_elem) if enabled_elem is not None else None
        )

        device_role = element.get("deviceRole")
        if device_role:
            try:
                instance.device_role = DeviceRole(device_role)
            except ValueError:
                instance.device_role = device_role
        else:
            instance.device_role = None

        loaded = element.get("loaded")
        instance.loaded = loaded.lower() == "true" if loaded else True

        instance.device_name = element.get("deviceName")
        instance.device_id = element.get("deviceID")
        instance.device_vendor = element.get("deviceVendor")

        state_elem = element.find("State")
        instance.state = (
            FileReference.from_xml(state_elem) if state_elem is not None else None
        )

        parameters_elem = element.find("Parameters")
        parameters = []
        if parameters_elem is not None:
            for param_elem in parameters_elem:
                param_cls = registry.resolve_parameter(param_elem.tag)
                if param_cls is not None:
                    parameters.append(param_cls.from_xml(param_elem))
        instance.automated_parameters = parameters

        return instance
