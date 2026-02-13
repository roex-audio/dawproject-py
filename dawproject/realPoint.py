"""RealPoint model -- a real-valued automation point."""

from .point import Point
from .doubleAdapter import DoubleAdapter
from .interpolation import Interpolation


class RealPoint(Point):
    """A real-valued automation point with optional interpolation.

    Attributes:
        time: Time position.
        value: The automation value.
        interpolation: Interpolation type (HOLD, LINEAR).
    """

    def __init__(self, time=None, value=None, interpolation=None):
        super().__init__(time)
        self.value = value
        self.interpolation = interpolation

    def to_xml(self):
        real_point_elem = super().to_xml()
        real_point_elem.tag = "RealPoint"
        if self.value is not None:
            real_point_elem.set("value", DoubleAdapter.to_xml(self.value))
        if self.interpolation is not None:
            real_point_elem.set("interpolation", self.interpolation.value)
        return real_point_elem

    @classmethod
    def from_xml(cls, element):
        instance = super().from_xml(element)
        instance.value = DoubleAdapter.from_xml(element.get("value"))
        interpolation = element.get("interpolation")
        instance.interpolation = Interpolation(interpolation) if interpolation else None
        return instance
