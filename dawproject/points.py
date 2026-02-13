"""Points model -- automation points on a timeline."""

from .timeline import Timeline
from .automationTarget import AutomationTarget


class Points(Timeline):
    """A collection of automation points targeting a parameter.

    Attributes:
        target: An AutomationTarget describing what parameter is automated.
        points: List of Point objects (RealPoint, etc.).
        unit: Optional unit string.
    """

    def __init__(
        self,
        target=None,
        points=None,
        unit=None,
        track=None,
        time_unit=None,
        name=None,
        color=None,
        comment=None,
    ):
        super().__init__(track, time_unit, name, color, comment)
        self.target = target if target else AutomationTarget()
        self.points = points if points else []
        self.unit = unit

    def to_xml(self):
        elem = super().to_xml()
        if self.unit is not None:
            elem.set("unit", self.unit)
        elem.append(self.target.to_xml())
        for point in self.points:
            elem.append(point.to_xml())
        return elem

    @classmethod
    def from_xml(cls, element):
        from . import registry

        instance = super().from_xml(element)

        instance.unit = element.get("unit")

        target_elem = element.find("Target")
        instance.target = (
            AutomationTarget.from_xml(target_elem)
            if target_elem is not None
            else AutomationTarget()
        )

        # Resolve point types via registry
        points = []
        point_tags = {"RealPoint", "EnumPoint", "BoolPoint", "IntegerPoint", "TimeSignaturePoint"}
        for child in element:
            if child.tag in point_tags:
                point_cls = registry.resolve_point(child.tag)
                if point_cls is not None:
                    points.append(point_cls.from_xml(child))
        instance.points = points

        return instance
