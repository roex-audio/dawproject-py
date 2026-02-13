"""AutomationTarget model -- identifies the target of an automation lane."""

from lxml import etree as ET

from .expressionType import ExpressionType


class AutomationTarget:
    """Identifies which parameter is targeted by automation points.

    Attributes:
        parameter: Parameter reference (resolved Referenceable, or ID string).
        expression: ExpressionType enum value.
        channel: MIDI channel number.
        key: MIDI key number.
        controller: MIDI controller number.
    """

    def __init__(
        self, parameter=None, expression=None, channel=None, key=None, controller=None
    ):
        self.parameter = parameter
        self.expression = expression
        self.channel = channel
        self.key = key
        self.controller = controller

    def to_xml(self):
        target_elem = ET.Element("Target")
        if self.parameter is not None:
            # IDREF pattern: serialize as the id string
            parameter_id = getattr(self.parameter, "id", None)
            if parameter_id is not None:
                target_elem.set("parameter", str(parameter_id))
            elif isinstance(self.parameter, str):
                target_elem.set("parameter", self.parameter)

        if self.expression is not None:
            expr_val = self.expression.value if isinstance(self.expression, ExpressionType) else str(self.expression)
            target_elem.set("expression", expr_val)
        if self.channel is not None:
            target_elem.set("channel", str(self.channel))
        if self.key is not None:
            target_elem.set("key", str(self.key))
        if self.controller is not None:
            target_elem.set("controller", str(self.controller))
        return target_elem

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return cls()

        from .referenceable import Referenceable

        # Resolve parameter IDREF
        parameter_str = element.get("parameter")
        parameter = None
        if parameter_str:
            resolved = Referenceable.get_by_id(parameter_str)
            parameter = resolved if resolved is not None else parameter_str

        # Resolve expression as ExpressionType enum
        expression_str = element.get("expression")
        expression = None
        if expression_str:
            try:
                expression = ExpressionType(expression_str)
            except ValueError:
                expression = expression_str

        channel = element.get("channel")
        channel = int(channel) if channel else None
        key = element.get("key")
        key = int(key) if key else None
        controller = element.get("controller")
        controller = int(controller) if controller else None
        return cls(parameter, expression, channel, key, controller)
