"""Referenceable model -- base class for objects with a unique ID."""

from .nameable import Nameable


class Referenceable(Nameable):
    """Base class for objects that can be referenced by ID.

    Maintains a class-level registry of all instances by ID,
    enabling cross-references (e.g. channel destinations, track references).

    Attributes:
        id: Unique string identifier (e.g. "id0", "id1").
    """

    ID = 0
    _instances = {}

    @classmethod
    def reset_id(cls):
        """Reset the ID counter and clear the instance registry."""
        cls.ID = 0
        cls._instances = {}

    def __init__(self, name=None, color=None, comment=None):
        super().__init__(name, color, comment)
        self.id = f"id{Referenceable.ID}"
        Referenceable._instances[self.id] = self
        Referenceable.ID += 1

    def to_xml(self):
        element = super().to_xml()
        element.set("id", self.id)
        return element

    @classmethod
    def from_xml(cls, element):
        """Create instance from XML, registering it by ID."""
        instance = super().from_xml(element)
        # Read ID from XML; generate one if missing
        xml_id = element.get("id") if element is not None else None
        if xml_id:
            instance.id = xml_id
            # Advance the counter past any loaded ID so that newly created
            # objects never collide with deserialized ones.
            try:
                num = int(xml_id.removeprefix("id"))
                if num >= Referenceable.ID:
                    Referenceable.ID = num + 1
            except (ValueError, AttributeError):
                pass
        else:
            instance.id = f"id{Referenceable.ID}"
            Referenceable.ID += 1
        Referenceable._instances[instance.id] = instance
        return instance

    @classmethod
    def get_by_id(cls, id):
        """Look up a Referenceable instance by its ID string."""
        return cls._instances.get(id)
