"""RealParameter model -- a numeric parameter with value, unit, and range."""

from .parameter import Parameter
from .doubleAdapter import DoubleAdapter
from .unit import Unit


class RealParameter(Parameter):
    """A real-valued (float) parameter with optional unit and min/max range.

    Attributes:
        value: The parameter value (float).
        unit: A Unit enum member describing the unit.
        min: Minimum allowed value.
        max: Maximum allowed value.
    """

    def __init__(self, value=None, unit=None, min_value=None, max_value=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.unit = unit
        self.min = min_value
        self.max = max_value

    def to_xml(self):
        param_elem = super().to_xml()
        param_elem.tag = "RealParameter"

        if self.value is not None:
            param_elem.set("value", DoubleAdapter.to_xml(self.value))
        if self.unit is not None:
            # Use .value to get the lowercase string (e.g. "linear", "bpm")
            param_elem.set("unit", self.unit.value)
        if self.min is not None:
            param_elem.set("min", DoubleAdapter.to_xml(self.min))
        if self.max is not None:
            param_elem.set("max", DoubleAdapter.to_xml(self.max))

        return param_elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return None

        instance = super().from_xml(element)
        instance.value = DoubleAdapter.from_xml(element.get("value"))

        unit_str = element.get("unit")
        instance.unit = Unit(unit_str) if unit_str else None

        instance.min = DoubleAdapter.from_xml(element.get("min"))
        instance.max = DoubleAdapter.from_xml(element.get("max"))

        return instance
