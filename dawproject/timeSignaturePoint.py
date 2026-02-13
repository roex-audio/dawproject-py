"""TimeSignaturePoint model -- a time-signature automation point."""

from .point import Point


class TimeSignaturePoint(Point):
    """A time-signature automation point.

    Attributes:
        time: Time position.
        numerator: Numerator of the time signature (e.g. 3 in 3/4).
        denominator: Denominator of the time signature (e.g. 4 in 3/4).
    """

    def __init__(self, time=None, numerator=None, denominator=None):
        super().__init__(time)
        self.numerator = numerator
        self.denominator = denominator

    def to_xml(self):
        elem = super().to_xml()
        elem.tag = "TimeSignaturePoint"
        if self.numerator is not None:
            elem.set("numerator", str(self.numerator))
        if self.denominator is not None:
            elem.set("denominator", str(self.denominator))
        return elem

    @classmethod
    def from_xml(cls, element):
        instance = super().from_xml(element)
        numerator = element.get("numerator")
        instance.numerator = int(numerator) if numerator is not None else None
        denominator = element.get("denominator")
        instance.denominator = int(denominator) if denominator is not None else None
        return instance
