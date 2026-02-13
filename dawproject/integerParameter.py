"""IntegerParameter model -- an integer-valued parameter."""

from .parameter import Parameter


class IntegerParameter(Parameter):
    """An integer parameter that can be used as an automation target.

    Attributes:
        value: Integer value for this parameter.
        min: Minimum value this parameter can have (inclusive).
        max: Maximum value this parameter can have (inclusive).
    """

    def __init__(self, value=None, min=None, max=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.min = min
        self.max = max

    def to_xml(self):
        elem = super().to_xml()
        if self.value is not None:
            elem.set("value", str(self.value))
        if self.min is not None:
            elem.set("min", str(self.min))
        if self.max is not None:
            elem.set("max", str(self.max))
        return elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return None
        instance = super().from_xml(element)
        value = element.get("value")
        instance.value = int(value) if value is not None else None
        min_val = element.get("min")
        instance.min = int(min_val) if min_val is not None else None
        max_val = element.get("max")
        instance.max = int(max_val) if max_val is not None else None
        return instance
