"""Equalizer model -- a built-in equalizer device."""

from lxml import etree as ET
from .builtInDevice import BuiltInDevice
from .realParameter import RealParameter
from .eqBand import EqBand
from .unit import Unit


class Equalizer(BuiltInDevice):
    """A built-in equalizer device with bands and input/output gain.

    Extends BuiltInDevice -> Device -> Referenceable, so it has an id,
    deviceName, deviceRole, enabled, etc. from the Device base class.

    Attributes:
        bands: List of EqBand objects.
        input_gain: RealParameter for input gain.
        output_gain: RealParameter for output gain.
    """

    def __init__(
        self,
        bands=None,
        input_gain=None,
        output_gain=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.bands = bands if bands is not None else []

        self.input_gain = (
            input_gain
            if isinstance(input_gain, RealParameter)
            else RealParameter(input_gain)
        )
        self.output_gain = (
            output_gain
            if isinstance(output_gain, RealParameter)
            else RealParameter(output_gain)
        )

    def to_xml(self):
        eq_elem = super().to_xml()

        # XSD order after device elements: Band*, InputGain?, OutputGain?
        for band in self.bands:
            eq_elem.append(band.to_xml())

        if self.input_gain is not None and self.input_gain.value is not None:
            ig_xml = self.input_gain.to_xml()
            ig_xml.tag = "InputGain"
            ig_xml.set("unit", Unit.DECIBEL.value)
            eq_elem.append(ig_xml)

        if self.output_gain is not None and self.output_gain.value is not None:
            og_xml = self.output_gain.to_xml()
            og_xml.tag = "OutputGain"
            og_xml.set("unit", Unit.DECIBEL.value)
            eq_elem.append(og_xml)

        return eq_elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return None

        # Parse Device-level attributes (id, deviceName, deviceRole, enabled, etc.)
        instance = super().from_xml(element)

        # Parse Equalizer-specific content
        bands = []
        for band_elem in element.findall("Band"):
            bands.append(EqBand.from_xml(band_elem))
        instance.bands = bands

        input_gain_elem = element.find("InputGain")
        instance.input_gain = (
            RealParameter.from_xml(input_gain_elem)
            if input_gain_elem is not None
            else RealParameter(None)
        )

        output_gain_elem = element.find("OutputGain")
        instance.output_gain = (
            RealParameter.from_xml(output_gain_elem)
            if output_gain_elem is not None
            else RealParameter(None)
        )

        return instance
