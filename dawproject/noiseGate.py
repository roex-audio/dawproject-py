"""NoiseGate model -- a built-in noise gate device."""

from .builtInDevice import BuiltInDevice
from .realParameter import RealParameter


class NoiseGate(BuiltInDevice):
    """A built-in noise gate device.

    Attributes:
        threshold: RealParameter for gate threshold.
        ratio: RealParameter for gate ratio.
        attack: RealParameter for attack time.
        release: RealParameter for release time.
        range: RealParameter for maximum gain reduction range [-inf to 0].
    """

    def __init__(
        self,
        threshold=None,
        ratio=None,
        attack=None,
        release=None,
        range_param=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.threshold = threshold
        self.ratio = ratio
        self.attack = attack
        self.release = release
        self.range = range_param

    def to_xml(self):
        elem = super().to_xml()
        elem.tag = "NoiseGate"

        # XSD alphabetical order: Attack, Range, Ratio, Release, Threshold
        if self.attack is not None and self.attack.value is not None:
            attack_xml = self.attack.to_xml()
            attack_xml.tag = "Attack"
            elem.append(attack_xml)

        if self.range is not None and self.range.value is not None:
            range_xml = self.range.to_xml()
            range_xml.tag = "Range"
            elem.append(range_xml)

        if self.ratio is not None and self.ratio.value is not None:
            ratio_xml = self.ratio.to_xml()
            ratio_xml.tag = "Ratio"
            elem.append(ratio_xml)

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

        instance.threshold = RealParameter.from_xml(element.find("Threshold"))
        instance.ratio = RealParameter.from_xml(element.find("Ratio"))
        instance.attack = RealParameter.from_xml(element.find("Attack"))
        instance.release = RealParameter.from_xml(element.find("Release"))
        instance.range = RealParameter.from_xml(element.find("Range"))

        return instance
