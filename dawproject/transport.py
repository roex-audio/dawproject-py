"""Transport model -- tempo and time signature."""

from lxml import etree as ET
from .realParameter import RealParameter
from .timeSignatureParameter import TimeSignatureParameter
from .unit import Unit


class Transport:
    """Transport information containing tempo and time signature.

    Attributes:
        tempo: RealParameter for tempo (BPM).
        time_signature: TimeSignatureParameter for the time signature.
    """

    def __init__(self, tempo=None, time_signature=None):
        self.tempo = tempo
        self.time_signature = time_signature

    def to_xml(self):
        transport_elem = ET.Element("Transport")

        if self.tempo is not None:
            tempo_xml = self.tempo.to_xml()
            tempo_xml.tag = "Tempo"
            # Ensure BPM unit is set
            if "unit" not in tempo_xml.attrib:
                tempo_xml.set("unit", Unit.BPM.value)
            transport_elem.append(tempo_xml)

        if self.time_signature is not None:
            ts_xml = self.time_signature.to_xml()
            ts_xml.tag = "TimeSignature"
            transport_elem.append(ts_xml)

        return transport_elem

    @classmethod
    def from_xml(cls, element):
        tempo_elem = element.find("Tempo")
        tempo = RealParameter.from_xml(tempo_elem) if tempo_elem is not None else None

        time_signature_elem = element.find("TimeSignature")
        time_signature = (
            TimeSignatureParameter.from_xml(time_signature_elem)
            if time_signature_elem is not None
            else None
        )

        return cls(tempo, time_signature)
