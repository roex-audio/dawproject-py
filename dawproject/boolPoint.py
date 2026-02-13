"""BoolPoint model -- a boolean automation point."""

from .point import Point


class BoolPoint(Point):
    """A boolean-valued automation point.

    Attributes:
        time: Time position.
        value: Boolean value of this point.
    """

    def __init__(self, time=None, value=None):
        super().__init__(time)
        self.value = value

    def to_xml(self):
        elem = super().to_xml()
        elem.tag = "BoolPoint"
        if self.value is not None:
            elem.set("value", str(self.value).lower())
        return elem

    @classmethod
    def from_xml(cls, element):
        instance = super().from_xml(element)
        value = element.get("value")
        instance.value = value.lower() == "true" if value is not None else None
        return instance
