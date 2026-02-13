"""TimeSignatureParameter model -- numerator/denominator time signature."""

from .parameter import Parameter


class TimeSignatureParameter(Parameter):
    """A time signature parameter with numerator and denominator.

    Extends Parameter, giving it an id (from Referenceable) and parameterID,
    making it usable as an automation target (matching the Java implementation).

    Attributes:
        numerator: The top number (e.g. 4 in 4/4).
        denominator: The bottom number (e.g. 4 in 4/4).
    """

    def __init__(self, numerator=None, denominator=None, **kwargs):
        super().__init__(**kwargs)
        self.numerator = numerator
        self.denominator = denominator

    def to_xml(self):
        elem = super().to_xml()
        if self.numerator is not None:
            elem.set("numerator", str(self.numerator))
        if self.denominator is not None:
            elem.set("denominator", str(self.denominator))
        return elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return cls()
        instance = super().from_xml(element)
        numerator = element.get("numerator")
        instance.numerator = int(numerator) if numerator is not None else None
        denominator = element.get("denominator")
        instance.denominator = int(denominator) if denominator is not None else None
        return instance
