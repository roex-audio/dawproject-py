"""Channel model -- a mixer channel with volume, pan, sends, and devices."""

from lxml import etree as ET
from .lane import Lane
from .realParameter import RealParameter
from .boolParameter import BoolParameter
from .mixerRole import MixerRole


class Channel(Lane):
    """A mixer channel within a Track.

    Attributes:
        role: MixerRole enum (REGULAR, MASTER, etc.) or string.
        audio_channels: Number of audio channels (default 2).
        volume: RealParameter for volume.
        pan: RealParameter for pan.
        mute: BoolParameter for mute state.
        solo: Boolean for solo state.
        destination: Reference to another Channel (output routing).
        sends: List of Send objects.
        devices: List of Device objects (EQ, compressor, etc.).
    """

    def __init__(
        self,
        role=None,
        audio_channels=2,
        volume=None,
        pan=None,
        mute=None,
        solo=None,
        destination=None,
        sends=None,
        devices=None,
        name=None,
        color=None,
        comment=None,
    ):
        super().__init__(name, color, comment)
        self.role = role
        self.audio_channels = audio_channels
        self.volume = volume
        self.pan = pan
        self.mute = mute
        self.solo = solo
        self.destination = destination
        self.sends = sends if sends else []
        self.devices = devices if devices else []

    def to_xml(self):
        channel_elem = super().to_xml()
        channel_elem.tag = "Channel"

        # Serialize role as enum value string
        if self.role is not None:
            role_val = self.role.value if isinstance(self.role, MixerRole) else str(self.role)
            channel_elem.set("role", role_val)

        if self.audio_channels is not None:
            channel_elem.set("audioChannels", str(self.audio_channels))

        if self.solo is not None:
            channel_elem.set("solo", str(self.solo).lower())

        if self.destination is not None:
            channel_elem.set("destination", str(self.destination.id))

        # XSD sequence order: Devices, Mute, Pan, Sends, Volume

        # 1. Devices
        if self.devices:
            devices_elem = ET.SubElement(channel_elem, "Devices")
            for device in self.devices:
                devices_elem.append(device.to_xml())

        # 2. Mute (directly as boolParameter element, not wrapped)
        if self.mute is not None:
            mute_xml = self.mute.to_xml()
            mute_xml.tag = "Mute"
            channel_elem.append(mute_xml)

        # 3. Pan
        if self.pan is not None:
            pan_xml = self.pan.to_xml()
            pan_xml.tag = "Pan"
            channel_elem.append(pan_xml)

        # 4. Sends
        if self.sends:
            sends_elem = ET.SubElement(channel_elem, "Sends")
            for send in self.sends:
                sends_elem.append(send.to_xml())

        # 5. Volume
        if self.volume is not None:
            vol_xml = self.volume.to_xml()
            vol_xml.tag = "Volume"
            channel_elem.append(vol_xml)

        return channel_elem

    @classmethod
    def from_xml(cls, element):
        from .send import Send
        from .device import Device
        from .referenceable import Referenceable

        instance = super().from_xml(element)

        role_str = element.get("role")
        if role_str:
            try:
                instance.role = MixerRole(role_str)
            except ValueError:
                instance.role = role_str
        else:
            instance.role = None

        audio_channels = element.get("audioChannels")
        instance.audio_channels = (
            int(audio_channels) if audio_channels is not None else 2
        )

        volume_elem = element.find("Volume")
        instance.volume = (
            RealParameter.from_xml(volume_elem) if volume_elem is not None else None
        )

        pan_elem = element.find("Pan")
        instance.pan = (
            RealParameter.from_xml(pan_elem) if pan_elem is not None else None
        )

        mute_elem = element.find("Mute")
        instance.mute = (
            BoolParameter.from_xml(mute_elem) if mute_elem is not None else None
        )

        solo = element.get("solo")
        instance.solo = solo.lower() == "true" if solo else None

        # Resolve destination via Referenceable registry
        destination_id = element.get("destination")
        instance.destination = (
            Referenceable.get_by_id(destination_id)
            if destination_id is not None
            else None
        )

        sends = []
        sends_elem = element.find("Sends")
        if sends_elem is not None:
            for send_elem in sends_elem.findall("Send"):
                sends.append(Send.from_xml(send_elem))
        instance.sends = sends

        devices = []
        devices_elem = element.find("Devices")
        if devices_elem is not None:
            from . import registry
            for device_elem in devices_elem:
                device_cls = registry.resolve_device(device_elem.tag)
                if device_cls is not None:
                    devices.append(device_cls.from_xml(device_elem))
                else:
                    devices.append(Device.from_xml(device_elem))
        instance.devices = devices

        return instance
