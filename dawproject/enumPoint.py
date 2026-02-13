"""EnumPoint model -- an enumerated automation point."""

from .point import Point


class EnumPoint(Point):
    """An enumerated automation point.

    Attributes:
        time: Time position.
        value: Integer index of the enum value.
    """

    def __init__(self, time=None, value=None):
        super().__init__(time)
        self.value = value

    def to_xml(self):
        elem = super().to_xml()
        elem.tag = "EnumPoint"
        if self.value is not None:
            elem.set("value", str(self.value))
        return elem

    @classmethod
    def from_xml(cls, element):
        instance = super().from_xml(element)
        value = element.get("value")
        instance.value = int(value) if value is not None else None
        return instance
