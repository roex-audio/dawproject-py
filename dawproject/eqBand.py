"""EqBand model -- a single EQ band with frequency, gain, Q, and type."""

from lxml import etree as ET
from .realParameter import RealParameter
from .boolParameter import BoolParameter
from .eqBandType import EqBandType
from .unit import Unit


class EqBand:
    """A single band of an equalizer.

    Attributes:
        freq: RealParameter for center frequency.
        gain: RealParameter for band gain.
        q: RealParameter for Q factor.
        enabled: BoolParameter for enabled state.
        band_type: EqBandType enum.
        order: Filter order (integer).
    """

    def __init__(
        self, freq=None, gain=None, q=None, enabled=None, band_type=None, order=None
    ):
        self.freq = freq if isinstance(freq, RealParameter) else RealParameter(freq)
        self.gain = gain if isinstance(gain, RealParameter) else RealParameter(gain)
        self.q = q if isinstance(q, RealParameter) else RealParameter(q)
        self.enabled = (
            enabled if isinstance(enabled, BoolParameter) else BoolParameter(enabled)
        )
        self.band_type = band_type
        self.order = order

    def to_xml(self):
        band_elem = ET.Element("Band")

        # XSD sequence order: Freq, Gain?, Q?, Enabled?
        if self.freq is not None:
            freq_xml = self.freq.to_xml()
            freq_xml.tag = "Freq"
            freq_xml.set("unit", Unit.HERTZ.value)
            band_elem.append(freq_xml)

        if self.gain is not None and self.gain.value is not None:
            gain_xml = self.gain.to_xml()
            gain_xml.tag = "Gain"
            gain_xml.set("unit", Unit.DECIBEL.value)
            band_elem.append(gain_xml)

        if self.q is not None and self.q.value is not None:
            q_xml = self.q.to_xml()
            q_xml.tag = "Q"
            q_xml.set("unit", Unit.LINEAR.value)
            band_elem.append(q_xml)

        if self.enabled is not None and self.enabled.value is not None:
            enabled_xml = self.enabled.to_xml()
            enabled_xml.tag = "Enabled"
            band_elem.append(enabled_xml)

        if self.band_type is not None:
            bt_val = self.band_type.value if isinstance(self.band_type, EqBandType) else str(self.band_type)
            band_elem.set("type", bt_val)
        if self.order is not None:
            band_elem.set("order", str(self.order))

        return band_elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return None

        freq = RealParameter.from_xml(element.find("Freq"))
        gain = RealParameter.from_xml(element.find("Gain"))
        q = RealParameter.from_xml(element.find("Q"))
        enabled = BoolParameter.from_xml(element.find("Enabled"))

        band_type = EqBandType(element.get("type")) if element.get("type") else None
        order = int(element.get("order")) if element.get("order") else None

        return cls(
            freq=freq, gain=gain, q=q, enabled=enabled, band_type=band_type, order=order
        )
