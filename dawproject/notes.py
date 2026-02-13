"""Notes model -- a container for Note objects on a timeline."""

from .timeline import Timeline
from .note import Note


class Notes(Timeline):
    """A timeline containing MIDI notes.

    Attributes:
        notes: List of Note objects.
    """

    def __init__(
        self,
        notes=None,
        track=None,
        time_unit=None,
        name=None,
        color=None,
        comment=None,
    ):
        super().__init__(track, time_unit, name, color, comment)
        self.notes = notes if notes else []

    def to_xml(self):
        elem = super().to_xml()
        for note in self.notes:
            elem.append(note.to_xml())
        return elem

    @classmethod
    def from_xml(cls, element):
        instance = super().from_xml(element)

        notes = []
        for note_elem in element.findall("Note"):
            notes.append(Note.from_xml(note_elem))
        instance.notes = notes

        return instance
