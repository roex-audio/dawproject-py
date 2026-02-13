"""DoubleAdapter -- conversion between Python floats and XML string representations."""


class DoubleAdapter:
    """Handles conversion between float values and XML strings,
    including special cases for infinity and None."""

    @staticmethod
    def to_xml(value: float) -> str:
        """Convert a float to an XML string representation.

        Handles inf, -inf, and None.
        """
        if value is None:
            return None
        if value == float("inf"):
            return "inf"
        elif value == float("-inf"):
            return "-inf"
        else:
            return str(float(value))

    @staticmethod
    def from_xml(value: str) -> float:
        """Convert an XML string to a float.

        Handles 'inf', '-inf', None, 'null', and empty strings.
        """
        if value is None or value in ("null", ""):
            return None
        if value == "inf":
            return float("inf")
        elif value == "-inf":
            return float("-inf")
        else:
            return float(value)
