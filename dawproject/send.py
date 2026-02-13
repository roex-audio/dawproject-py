"""Send model -- an auxiliary bus send from a channel."""

from lxml import etree as ET
from .referenceable import Referenceable
from .sendType import SendType
from .realParameter import RealParameter


class Send(Referenceable):
    """A send routing from one channel to another.

    Attributes:
        volume: RealParameter for send level.
        pan: RealParameter for send pan.
        type: SendType (PRE or POST).
        destination: The destination Channel.
    """

    def __init__(
        self,
        volume=None,
        pan=None,
        type=SendType.POST,
        destination=None,
        name=None,
        color=None,
        comment=None,
    ):
        super().__init__(name, color, comment)
        self.volume = volume
        self.pan = pan
        self.type = type
        self.destination = destination

    def to_xml(self):
        send_elem = super().to_xml()
        send_elem.tag = "Send"

        # Serialize type as enum value string
        if self.type is not None:
            type_val = self.type.value if isinstance(self.type, SendType) else str(self.type)
            send_elem.set("type", type_val)

        if self.destination is not None:
            send_elem.set("destination", str(self.destination.id))

        # XSD sequence order: Pan, Volume
        if self.pan is not None:
            pan_xml = self.pan.to_xml()
            pan_xml.tag = "Pan"
            send_elem.append(pan_xml)

        if self.volume is not None:
            vol_xml = self.volume.to_xml()
            vol_xml.tag = "Volume"
            send_elem.append(vol_xml)

        return send_elem

    @classmethod
    def from_xml(cls, element):
        instance = super().from_xml(element)

        volume_elem = element.find("Volume")
        instance.volume = (
            RealParameter.from_xml(volume_elem) if volume_elem is not None else None
        )

        pan_elem = element.find("Pan")
        instance.pan = (
            RealParameter.from_xml(pan_elem) if pan_elem is not None else None
        )

        type_str = element.get("type")
        instance.type = SendType(type_str) if type_str else SendType.POST

        destination_id = element.get("destination")
        if destination_id is not None:
            instance.destination = Referenceable.get_by_id(destination_id)
        else:
            instance.destination = None

        return instance
