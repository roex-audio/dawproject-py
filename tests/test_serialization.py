"""Tests for XML serialization (to_xml) of DAWproject models."""

import pytest
from lxml import etree as ET
from dawproject import (
    Project, Application, Transport, Track, Channel,
    Arrangement, Lanes, Clips, Clip, Audio, Notes, Note,
    Markers, Marker, Points, RealPoint, Warps, Warp,
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


class TestProjectSerialization:
    def test_project_xml_structure(self):
        project = Project()
        project.application = Application(name="Test", version="1.0")
        root = project.to_xml()

        assert root.tag == "Project"
        assert root.get("version") == "1.0"
        assert root.find("Application") is not None
        assert root.find("Application").get("name") == "Test"

    def test_project_with_transport(self):
        project = Project()
        project.transport = Transport(
            tempo=RealParameter(value=140.0, unit=Unit.BPM),
            time_signature=TimeSignatureParameter(numerator=3, denominator=4),
        )
        root = project.to_xml()

        transport = root.find("Transport")
        assert transport is not None
        assert transport.find("Tempo") is not None
        assert transport.find("Tempo").get("value") == "140.0"
        assert transport.find("TimeSignature").get("numerator") == "3"

    def test_project_with_structure(self):
        project = Project()
        project.structure.append(
            Track(name="Track1", loaded=True, content_type={ContentType.AUDIO})
        )
        root = project.to_xml()

        structure = root.find("Structure")
        assert structure is not None
        tracks = structure.findall("Track")
        assert len(tracks) == 1
        assert tracks[0].get("name") == "Track1"
        assert tracks[0].get("contentType") == "audio"
        assert tracks[0].get("loaded") == "true"


class TestTrackSerialization:
    def test_track_with_channel(self):
        channel = Channel(
            volume=RealParameter(value=0.8, unit=Unit.LINEAR),
            pan=RealParameter(value=0.5, unit=Unit.NORMALIZED),
            role=MixerRole.REGULAR,
        )
        track = Track(name="Lead", channel=channel, content_type={ContentType.AUDIO})
        elem = track.to_xml()

        assert elem.tag == "Track"
        assert elem.get("name") == "Lead"
        assert elem.get("contentType") == "audio"

        ch = elem.find("Channel")
        assert ch is not None
        assert ch.get("role") == "regular"

    def test_channel_role_serializes_as_value(self):
        channel = Channel(role=MixerRole.MASTER)
        elem = channel.to_xml()
        assert elem.get("role") == "master"

    def test_channel_destination(self):
        master_ch = Channel(role=MixerRole.MASTER)
        regular_ch = Channel(role=MixerRole.REGULAR, destination=master_ch)
        elem = regular_ch.to_xml()
        assert elem.get("destination") == master_ch.id


class TestParameterSerialization:
    def test_real_parameter_unit_value(self):
        param = RealParameter(value=1.0, unit=Unit.LINEAR)
        elem = param.to_xml()
        assert elem.get("unit") == "linear"  # Not "LINEAR"
        assert elem.get("value") == "1.0"

    def test_real_parameter_bpm(self):
        param = RealParameter(value=120.0, unit=Unit.BPM)
        elem = param.to_xml()
        assert elem.get("unit") == "bpm"

    def test_bool_parameter(self):
        param = BoolParameter(value=True)
        elem = param.to_xml()
        assert elem.get("value") == "true"

    def test_real_parameter_with_range(self):
        param = RealParameter(value=440.0, unit=Unit.HERTZ, min_value=20.0, max_value=20000.0)
        elem = param.to_xml()
        assert elem.get("min") == "20.0"
        assert elem.get("max") == "20000.0"


class TestClipSerialization:
    def test_clip_with_audio(self):
        audio = Audio(
            sample_rate=44100, channels=2, duration=5.0,
            file=FileReference(path="test.wav"),
        )
        clip = Clip(time=0, duration=5.0, content=audio)
        elem = clip.to_xml()

        assert elem.tag == "Clip"
        assert elem.get("time") == "0.0"
        assert elem.get("duration") == "5.0"

        audio_elem = elem.find("Audio")
        assert audio_elem is not None
        assert audio_elem.get("sampleRate") == "44100"
        assert audio_elem.find("File").get("path") == "test.wav"


class TestEqualizerSerialization:
    def test_equalizer_xml(self):
        eq = Equalizer(
            device_name="EQ_1",
            device_role="audioFX",
            bands=[EqBand(freq=1000, gain=3, q=1.0, enabled=True, band_type=EqBandType.BELL)],
            input_gain=RealParameter(value=0.0, unit=Unit.DECIBEL),
            output_gain=RealParameter(value=0.0, unit=Unit.DECIBEL),
        )
        elem = eq.to_xml()

        assert elem.tag == "Equalizer"
        assert elem.get("deviceName") == "EQ_1"
        assert elem.get("deviceRole") == "audioFX"

        bands = elem.findall("Band")
        assert len(bands) == 1
        assert bands[0].get("type") == "bell"

        # Gain elements should have attributes
        input_gain = elem.find("InputGain")
        assert input_gain is not None
        assert input_gain.get("unit") == "decibel"


class TestCompressorSerialization:
    def test_compressor_xml(self):
        comp = Compressor(
            device_name="Comp_1",
            device_role="audioFX",
            threshold=-20,
            ratio=4.0,
            attack=0.01,
            release=0.1,
            input_gain=0.0,
            output_gain=0.0,
            auto_makeup=True,
        )
        elem = comp.to_xml()

        assert elem.tag == "Compressor"
        assert elem.get("deviceName") == "Comp_1"
        assert elem.find("Threshold") is not None
        assert float(elem.find("Threshold").get("value")) == -20.0
        assert elem.find("AutoMakeup").get("value") == "true"


class TestMetaDataSerialization:
    def test_metadata_xml(self):
        meta = MetaData(title="Song", artist="Artist", year="2025")
        elem = meta.to_xml()

        assert elem.tag == "MetaData"
        assert elem.findtext("Title") == "Song"
        assert elem.findtext("Artist") == "Artist"
        assert elem.findtext("Year") == "2025"

    def test_metadata_empty(self):
        meta = MetaData()
        elem = meta.to_xml()
        assert len(list(elem)) == 0


class TestSendSerialization:
    def test_send_type(self):
        send = Send(type=SendType.PRE)
        elem = send.to_xml()
        assert elem.get("type") == "pre"

    def test_send_default_type(self):
        send = Send()
        elem = send.to_xml()
        assert elem.get("type") == "post"


class TestNotesSerialization:
    def test_notes_with_notes(self):
        n = Note(time=0.0, duration=1.0, key=60, vel=100)
        notes = Notes(notes=[n])
        elem = notes.to_xml()

        assert elem.tag == "Notes"
        note_elems = elem.findall("Note")
        assert len(note_elems) == 1
        assert note_elems[0].get("key") == "60"


class TestRealPointSerialization:
    def test_real_point(self):
        pt = RealPoint(time=1.0, value=0.5, interpolation=Interpolation.LINEAR)
        elem = pt.to_xml()

        assert elem.tag == "RealPoint"
        assert elem.get("time") == "1.0"
        assert elem.get("value") == "0.5"
        assert elem.get("interpolation") == "linear"


class TestWarpsSerialization:
    def test_warps_with_content_time_unit(self):
        audio = Audio(
            sample_rate=44100, channels=1, duration=4.657,
            file=FileReference(path="samples/dummy.wav"),
            time_unit=TimeUnit.SECONDS,
        )
        warps = Warps(
            content=audio,
            content_time_unit=TimeUnit.SECONDS,
            time_unit=TimeUnit.BEATS,
            events=[Warp(time=0, content_time=0), Warp(time=8, content_time=4.657)],
        )
        elem = warps.to_xml()

        assert elem.tag == "Warps"
        assert elem.get("contentTimeUnit") == "seconds"
        assert elem.find("Audio") is not None
        warp_elems = elem.findall("Warp")
        assert len(warp_elems) == 2

    def test_warps_to_xml_raises_when_content_time_unit_is_none(self):
        warps = Warps(content_time_unit=None)
        with pytest.raises(ValueError, match="content_time_unit is required"):
            warps.to_xml()
