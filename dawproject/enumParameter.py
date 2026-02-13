"""EnumParameter model -- an enumerated parameter."""

from .parameter import Parameter


class EnumParameter(Parameter):
    """An enumerated parameter that can be used as an automation target.

    Attributes:
        value: Index of the enum value.
        count: Number of entries in the enum. value will be in the range [0 .. count-1].
        labels: Labels of the individual enum values (space-separated in XML).
    """

    def __init__(self, value=None, count=None, labels=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.count = count
        self.labels = labels if labels is not None else []

    def to_xml(self):
        elem = super().to_xml()
        if self.value is not None:
            elem.set("value", str(self.value))
        if self.count is not None:
            elem.set("count", str(self.count))
        if self.labels:
            elem.set("labels", " ".join(self.labels))
        return elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return None
        instance = super().from_xml(element)
        value = element.get("value")
        instance.value = int(value) if value is not None else None
        count = element.get("count")
        instance.count = int(count) if count is not None else None
        labels_str = element.get("labels")
        instance.labels = labels_str.split() if labels_str else []
        return instance
