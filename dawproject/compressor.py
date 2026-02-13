"""Compressor model -- a built-in compressor device."""

from lxml import etree as ET
from .builtInDevice import BuiltinDevice
from .realParameter import RealParameter
from .boolParameter import BoolParameter
from .unit import Unit


class Compressor(BuiltinDevice):
    """A built-in compressor device with threshold, ratio, attack, release, and gain.

    Extends BuiltinDevice -> Device -> Referenceable, so it has an id,
    deviceName, deviceRole, enabled, etc. from the Device base class.

    Attributes:
        threshold: RealParameter for compressor threshold.
        ratio: RealParameter for compression ratio.
        attack: RealParameter for attack time.
        release: RealParameter for release time.
        input_gain: RealParameter for input gain.
        output_gain: RealParameter for output gain.
        auto_makeup: BoolParameter for automatic makeup gain.
    """

    def __init__(
        self,
        threshold=None,
        ratio=None,
        attack=None,
        release=None,
        input_gain=None,
        output_gain=None,
        auto_makeup=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.threshold = (
            threshold
            if isinstance(threshold, RealParameter)
            else RealParameter(threshold)
        )
        self.ratio = ratio if isinstance(ratio, RealParameter) else RealParameter(ratio)
        self.attack = (
            attack if isinstance(attack, RealParameter) else RealParameter(attack)
        )
        self.release = (
            release if isinstance(release, RealParameter) else RealParameter(release)
        )
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
        self.auto_makeup = (
            auto_makeup
            if isinstance(auto_makeup, BoolParameter)
            else BoolParameter(auto_makeup)
        )

    def to_xml(self):
        comp_elem = super().to_xml()

        # XSD order after device elements: Attack, AutoMakeup, InputGain,
        # OutputGain, Ratio, Release, Threshold
        def add_param(parent, tag, param, unit):
            if param is not None and param.value is not None:
                param_xml = param.to_xml()
                param_xml.tag = tag
                param_xml.set("unit", unit)
                parent.append(param_xml)

        add_param(comp_elem, "Attack", self.attack, Unit.SECONDS.value)

        if self.auto_makeup is not None and self.auto_makeup.value is not None:
            am_xml = self.auto_makeup.to_xml()
            am_xml.tag = "AutoMakeup"
            comp_elem.append(am_xml)

        add_param(comp_elem, "InputGain", self.input_gain, Unit.DECIBEL.value)
        add_param(comp_elem, "OutputGain", self.output_gain, Unit.DECIBEL.value)
        add_param(comp_elem, "Ratio", self.ratio, Unit.PERCENT.value)
        add_param(comp_elem, "Release", self.release, Unit.SECONDS.value)
        add_param(comp_elem, "Threshold", self.threshold, Unit.DECIBEL.value)

        return comp_elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return None

        # Parse Device-level attributes (id, deviceName, deviceRole, enabled, etc.)
        instance = super().from_xml(element)

        # Parse Compressor-specific content (wrap None -> default param to avoid
        # AttributeError when callers access .value on missing optional elements)
        instance.threshold = RealParameter.from_xml(element.find("Threshold")) or RealParameter(None)
        instance.ratio = RealParameter.from_xml(element.find("Ratio")) or RealParameter(None)
        instance.attack = RealParameter.from_xml(element.find("Attack")) or RealParameter(None)
        instance.release = RealParameter.from_xml(element.find("Release")) or RealParameter(None)
        instance.input_gain = RealParameter.from_xml(element.find("InputGain")) or RealParameter(None)
        instance.output_gain = RealParameter.from_xml(element.find("OutputGain")) or RealParameter(None)
        instance.auto_makeup = BoolParameter.from_xml(element.find("AutoMakeup")) or BoolParameter(None)

        return instance
