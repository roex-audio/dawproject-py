"""BoolParameter model -- a boolean-valued parameter."""

from .parameter import Parameter


class BoolParameter(Parameter):
    """A boolean parameter.

    Attributes:
        value: Boolean value (True/False).
    """

    def __init__(
        self, value=None, parameter_id=None, name=None, color=None, comment=None
    ):
        super().__init__(parameter_id, name, color, comment)
        self.value = value

    def to_xml(self):
        bool_param_elem = super().to_xml()
        bool_param_elem.tag = "BoolParameter"
        if self.value is not None:
            bool_param_elem.set("value", str(self.value).lower())
        return bool_param_elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return None
        instance = super().from_xml(element)
        value = element.get("value")
        instance.value = value.lower() == "true" if value else None
        return instance
