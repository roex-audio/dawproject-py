"""Limiter model -- a built-in limiter device."""

from .builtInDevice import BuiltinDevice
from .realParameter import RealParameter


class Limiter(BuiltinDevice):
    """A built-in limiter device.

    Attributes:
        threshold: RealParameter for limiter threshold.
        input_gain: RealParameter for input gain.
        output_gain: RealParameter for output gain.
        attack: RealParameter for attack time.
        release: RealParameter for release time.
    """

    def __init__(
        self,
        threshold=None,
        input_gain=None,
        output_gain=None,
        attack=None,
        release=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.threshold = (
            threshold
            if isinstance(threshold, RealParameter)
            else RealParameter(threshold)
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
        self.attack = (
            attack
            if isinstance(attack, RealParameter)
            else RealParameter(attack)
        )
        self.release = (
            release
            if isinstance(release, RealParameter)
            else RealParameter(release)
        )

    def to_xml(self):
        elem = super().to_xml()
        elem.tag = "Limiter"

        # XSD alphabetical order: Attack, InputGain, OutputGain, Release, Threshold
        if self.attack is not None and self.attack.value is not None:
            attack_xml = self.attack.to_xml()
            attack_xml.tag = "Attack"
            elem.append(attack_xml)

        if self.input_gain is not None and self.input_gain.value is not None:
            ig_xml = self.input_gain.to_xml()
            ig_xml.tag = "InputGain"
            elem.append(ig_xml)

        if self.output_gain is not None and self.output_gain.value is not None:
            og_xml = self.output_gain.to_xml()
            og_xml.tag = "OutputGain"
            elem.append(og_xml)

        if self.release is not None and self.release.value is not None:
            release_xml = self.release.to_xml()
            release_xml.tag = "Release"
            elem.append(release_xml)

        if self.threshold is not None and self.threshold.value is not None:
            threshold_xml = self.threshold.to_xml()
            threshold_xml.tag = "Threshold"
            elem.append(threshold_xml)

        return elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return None

        instance = super().from_xml(element)

        instance.threshold = RealParameter.from_xml(element.find("Threshold")) or RealParameter(None)
        instance.input_gain = RealParameter.from_xml(element.find("InputGain")) or RealParameter(None)
        instance.output_gain = RealParameter.from_xml(element.find("OutputGain")) or RealParameter(None)
        instance.attack = RealParameter.from_xml(element.find("Attack")) or RealParameter(None)
        instance.release = RealParameter.from_xml(element.find("Release")) or RealParameter(None)

        return instance
