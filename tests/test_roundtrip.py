"""End-to-end round-trip tests: create -> serialize -> deserialize -> verify."""

import pytest
from lxml import etree as ET
from dawproject import (
    Project, Application, Transport, Track, Channel,
    Arrangement, Lanes, Clips, Clip, Audio, Notes, Note,
    Markers, Marker, Points, RealPoint,
    RealParameter, BoolParameter, TimeSignatureParameter,
    AutomationTarget, Equalizer, Compressor, EqBand, Send,
    ContentType, MixerRole, TimeUnit, Unit, DeviceRole,
    EqBandType, Interpolation, SendType,
    Utility, Referenceable, FileReference, MetaData,
)


@pytest.fixture(autouse=True)
def reset_ids():
    Referenceable.reset_id()
    yield
    Referenceable.reset_id()


def roundtrip_project(project):
    """Serialize and deserialize a Project, returning the deserialized version."""
    root = project.to_xml()
    xml_str = ET.tostring(root, pretty_print=True, encoding="unicode")

    Referenceable.reset_id()
    root2 = ET.fromstring(xml_str)
    return Project.from_xml(root2)


class TestBasicRoundTrip:
    def test_empty_project(self):
        project = Project()
        project.application = Application(name="Test", version="1.0")
        result = roundtrip_project(project)

        assert result.version == "1.0"
        assert result.application.name == "Test"
        assert result.structure == []
        assert result.arrangement is None

    def test_project_with_transport(self):
        project = Project()
        project.application = Application(name="Test", version="1.0")
        project.transport = Transport(
            tempo=RealParameter(value=120.0, unit=Unit.BPM),
            time_signature=TimeSignatureParameter(numerator=4, denominator=4),
        )
        result = roundtrip_project(project)

        assert result.transport is not None
        assert result.transport.tempo.value == 120.0
        assert result.transport.tempo.unit == Unit.BPM
        assert result.transport.time_signature.numerator == 4
        assert result.transport.time_signature.denominator == 4


class TestStructureRoundTrip:
    def test_master_and_audio_tracks(self):
        project = Project()
        project.application = Application(name="Test", version="1.0")

        master = Utility.create_track("Master", set(), MixerRole.MASTER, 1.0, 0.5)
        audio = Utility.create_track("Lead", {ContentType.AUDIO}, MixerRole.REGULAR, 0.8, 0.3)
        audio.channel.destination = master.channel

        project.structure = [master, audio]
        result = roundtrip_project(project)

        assert len(result.structure) == 2

        r_master = result.structure[0]
        assert r_master.name == "Master"
        assert r_master.channel.role == MixerRole.MASTER
        assert r_master.channel.volume.value == 1.0

        r_audio = result.structure[1]
        assert r_audio.name == "Lead"
        assert r_audio.channel.role == MixerRole.REGULAR
        assert r_audio.channel.volume.value == 0.8
        assert ContentType.AUDIO in r_audio.content_type

    def test_nested_tracks(self):
        project = Project()
        project.application = Application(name="Test", version="1.0")

        group = Track(name="Drums")
        kick = Track(name="Kick", content_type={ContentType.AUDIO})
        snare = Track(name="Snare", content_type={ContentType.AUDIO})
        group.tracks = [kick, snare]

        project.structure = [group]
        result = roundtrip_project(project)

        assert len(result.structure) == 1
        assert result.structure[0].name == "Drums"
        assert len(result.structure[0].tracks) == 2
        assert result.structure[0].tracks[0].name == "Kick"
        assert result.structure[0].tracks[1].name == "Snare"


class TestArrangementRoundTrip:
    def test_arrangement_with_clips(self):
        project = Project()
        project.application = Application(name="Test", version="1.0")

        track = Utility.create_track("Lead", {ContentType.AUDIO}, MixerRole.REGULAR, 0.8, 0.5)
        project.structure.append(track)

        audio_content = Utility.create_audio("test.wav", 44100, 2, 10.0)
        clip = Utility.create_clip(audio_content, 0, 10.0)
        clips = Utility.create_clips(clip)
        clips.track = track

        project.arrangement = Arrangement()
        project.arrangement.lanes = Lanes()
        project.arrangement.lanes.time_unit = TimeUnit.SECONDS
        project.arrangement.lanes.lanes.append(clips)

        result = roundtrip_project(project)

        assert result.arrangement is not None
        assert result.arrangement.lanes is not None
        assert result.arrangement.lanes.time_unit == TimeUnit.SECONDS
        assert len(result.arrangement.lanes.lanes) == 1

        r_clips = result.arrangement.lanes.lanes[0]
        assert isinstance(r_clips, Clips)
        assert len(r_clips.clips) == 1
        assert isinstance(r_clips.clips[0].content, Audio)
        assert r_clips.clips[0].content.sample_rate == 44100
        assert r_clips.clips[0].content.file.path == "test.wav"


class TestDeviceRoundTrip:
    def test_equalizer_roundtrip(self):
        project = Project()
        project.application = Application(name="Test", version="1.0")

        track = Utility.create_track("Lead", {ContentType.AUDIO}, MixerRole.REGULAR, 0.8, 0.5)
        eq = Equalizer(
            device_name="EQ_1",
            device_role=DeviceRole.AUDIO_FX.value,
            bands=[EqBand(freq=1000, gain=3.0, q=1.0, enabled=True, band_type=EqBandType.BELL)],
        )
        track.channel.devices.append(eq)
        project.structure.append(track)

        result = roundtrip_project(project)

        r_track = result.structure[0]
        assert len(r_track.channel.devices) == 1

    def test_compressor_roundtrip(self):
        project = Project()
        project.application = Application(name="Test", version="1.0")

        track = Utility.create_track("Vocals", {ContentType.AUDIO}, MixerRole.REGULAR, 0.8, 0.5)
        comp = Compressor(
            device_name="Comp_1",
            device_role=DeviceRole.AUDIO_FX.value,
            threshold=-20,
            ratio=4.0,
            attack=0.01,
            release=0.2,
            input_gain=0.0,
            output_gain=0.0,
            auto_makeup=True,
        )
        track.channel.devices.append(comp)
        project.structure.append(track)

        result = roundtrip_project(project)

        r_track = result.structure[0]
        assert len(r_track.channel.devices) == 1


class TestMetaDataRoundTrip:
    def test_metadata_roundtrip(self):
        meta = MetaData(
            title="My Song",
            artist="Test Artist",
            album="Test Album",
            year="2025",
            genre="Electronic",
            copyright="(C) 2025",
        )
        root = meta.to_xml()
        xml_str = ET.tostring(root, encoding="unicode")
        root2 = ET.fromstring(xml_str)
        result = MetaData.from_xml(root2)

        assert result.title == "My Song"
        assert result.artist == "Test Artist"
        assert result.album == "Test Album"
        assert result.year == "2025"
        assert result.genre == "Electronic"
        assert result.copyright == "(C) 2025"


class TestNotesRoundTrip:
    def test_notes_roundtrip(self):
        notes = Notes(notes=[
            Note(time=0.0, duration=1.0, key=60, vel=100),
            Note(time=1.0, duration=0.5, key=64, vel=80),
            Note(time=1.5, duration=0.5, key=67, vel=90),
        ])

        elem = notes.to_xml()
        xml_str = ET.tostring(elem, encoding="unicode")
        Referenceable.reset_id()
        elem2 = ET.fromstring(xml_str)
        result = Notes.from_xml(elem2)

        assert len(result.notes) == 3
        assert result.notes[0].key == 60
        assert result.notes[1].key == 64
        assert result.notes[2].key == 67
        assert result.notes[0].vel == 100.0
