from classes.dawProject import DawProject  # current API

def test_smoke_has_dawproject():
    assert hasattr(DawProject, "load") or hasattr(DawProject, "save_xml")
