"""Arrangement model -- the main timeline arrangement."""

from lxml import etree as ET
from .referenceable import Referenceable


class Arrangement(Referenceable):
    """The project arrangement containing lanes, markers, and automation.

    Attributes:
        time_signature_automation: Points for time signature automation.
        tempo_automation: Points for tempo automation.
        markers: A Markers timeline.
        lanes: A Lanes timeline containing the arrangement content.
    """

    def __init__(
        self,
        time_signature_automation=None,
        tempo_automation=None,
        markers=None,
        lanes=None,
    ):
        super().__init__()
        self.time_signature_automation = time_signature_automation
        self.tempo_automation = tempo_automation
        self.markers = markers
        self.lanes = lanes

    def to_xml(self):
        arrangement_elem = ET.Element("Arrangement")

        # XSD sequence order: Lanes, Markers, TempoAutomation, TimeSignatureAutomation
        if self.lanes is not None:
            arrangement_elem.append(self.lanes.to_xml())

        if self.markers is not None:
            arrangement_elem.append(self.markers.to_xml())

        if self.tempo_automation is not None:
            tempo_elem = self.tempo_automation.to_xml()
            tempo_elem.tag = "TempoAutomation"
            arrangement_elem.append(tempo_elem)

        if self.time_signature_automation is not None:
            ts_elem = self.time_signature_automation.to_xml()
            ts_elem.tag = "TimeSignatureAutomation"
            arrangement_elem.append(ts_elem)

        return arrangement_elem

    @classmethod
    def from_xml(cls, element):
        from .points import Points
        from .markers import Markers
        from .lanes import Lanes

        ts_automation_elem = element.find("TimeSignatureAutomation")
        time_signature_automation = (
            Points.from_xml(ts_automation_elem)
            if ts_automation_elem is not None
            else None
        )

        tempo_automation_elem = element.find("TempoAutomation")
        tempo_automation = (
            Points.from_xml(tempo_automation_elem)
            if tempo_automation_elem is not None
            else None
        )

        markers_elem = element.find("Markers")
        markers = Markers.from_xml(markers_elem) if markers_elem is not None else None

        lanes_elem = element.find("Lanes")
        lanes = Lanes.from_xml(lanes_elem) if lanes_elem is not None else None

        return cls(time_signature_automation, tempo_automation, markers, lanes)
