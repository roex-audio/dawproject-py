"""Tests for creating DAWproject model objects."""

import pytest
from dawproject import (
    Project, Application, Transport, Track, Channel, Lane,
    Arrangement, Scene, Send, Clip, Audio, Lanes, Clips, Notes, Note,
    Markers, Marker, Points, Warps, Warp, MediaFile,
    RealParameter, BoolParameter, Parameter, TimeSignatureParameter,
    AutomationTarget, Device, BuiltInDevice, Equalizer, Compressor, EqBand,
    ContentType, MixerRole, TimeUnit, Unit, Interpolation, SendType,
    DeviceRole, EqBandType, ExpressionType,
    Utility, Referenceable, FileReference, DoubleAdapter, RealPoint, Point,
    MetaData,
)


@pytest.fixture(autouse=True)
def reset_ids():
    """Reset Referenceable IDs before each test."""
    Referenceable.reset_id()
    yield
    Referenceable.reset_id()


class TestProject:
    def test_default_project(self):
        project = Project()
        assert project.version == "1.0"
        assert project.application is not None
        assert project.structure == []
        assert project.scenes == []
        assert project.transport is None
        assert project.arrangement is None

    def test_project_with_application(self):
        app = Application(name="TestDAW", version="2.0")
        project = Project(application=app)
        assert project.application.name == "TestDAW"
        assert project.application.version == "2.0"


class TestTrack:
    def test_create_track(self):
        track = Track(name="Bass", loaded=True)
        assert track.name == "Bass"
        assert track.loaded is True
        assert track.content_type == []
        assert track.tracks == []

    def test_track_with_channel(self):
        channel = Channel(
            volume=RealParameter(value=0.8, unit=Unit.LINEAR),
            pan=RealParameter(value=0.5, unit=Unit.NORMALIZED),
            role=MixerRole.REGULAR,
        )
        track = Track(name="Lead", channel=channel, content_type={ContentType.AUDIO})
        assert track.channel.role == MixerRole.REGULAR
        assert track.channel.volume.value == 0.8

    def test_nested_tracks(self):
        parent = Track(name="Group")
        child1 = Track(name="Child1")
        child2 = Track(name="Child2")
        parent.tracks = [child1, child2]
        assert len(parent.tracks) == 2


class TestChannel:
    def test_default_channel(self):
        channel = Channel()
        assert channel.role is None
        assert channel.audio_channels == 2
        assert channel.sends == []
        assert channel.devices == []

    def test_channel_with_role(self):
        channel = Channel(role=MixerRole.MASTER)
        assert channel.role == MixerRole.MASTER

    def test_channel_destination(self):
        master = Channel(role=MixerRole.MASTER)
        regular = Channel(role=MixerRole.REGULAR, destination=master)
        assert regular.destination is master


class TestRealParameter:
    def test_create_with_value_and_unit(self):
        param = RealParameter(value=0.5, unit=Unit.LINEAR)
        assert param.value == 0.5
        assert param.unit == Unit.LINEAR

    def test_create_with_range(self):
        param = RealParameter(value=100, unit=Unit.HERTZ, min_value=20, max_value=20000)
        assert param.min == 20
        assert param.max == 20000


class TestBoolParameter:
    def test_create_true(self):
        param = BoolParameter(value=True)
        assert param.value is True

    def test_create_false(self):
        param = BoolParameter(value=False)
        assert param.value is False


class TestClip:
    def test_create_clip(self):
        audio = Audio(sample_rate=44100, channels=2, duration=5.0)
        clip = Clip(time=0, duration=5.0, content=audio)
        assert clip.time == 0
        assert clip.duration == 5.0
        assert isinstance(clip.content, Audio)

    def test_clip_with_time_units(self):
        clip = Clip(
            time=0,
            duration=10.0,
            content_time_unit=TimeUnit.SECONDS,
            fade_time_unit=TimeUnit.SECONDS,
            fade_in_time=0.1,
            fade_out_time=0.2,
        )
        assert clip.content_time_unit == TimeUnit.SECONDS
        assert clip.fade_in_time == 0.1


class TestAudio:
    def test_create_audio(self):
        audio = Audio(
            sample_rate=48000, channels=1, duration=30.0,
            file=FileReference(path="vocal.wav"),
        )
        assert audio.sample_rate == 48000
        assert audio.channels == 1
        assert audio.duration == 30.0
        assert audio.file.path == "vocal.wav"


class TestNote:
    def test_create_note(self):
        note = Note(time=0.0, duration=1.0, key=60, vel=100)
        assert note.key == 60
        assert note.vel == 100
        assert note.channel == 0


class TestMarker:
    def test_create_marker(self):
        marker = Marker(time=10.0, name="Verse")
        assert marker.time == 10.0
        assert marker.name == "Verse"


class TestSend:
    def test_default_type(self):
        send = Send()
        assert send.type == SendType.POST

    def test_pre_send(self):
        send = Send(type=SendType.PRE)
        assert send.type == SendType.PRE


class TestEqualizer:
    def test_create_equalizer(self):
        eq = Equalizer(
            device_name="EQ1",
            device_role="audioFX",
            bands=[EqBand(freq=1000, gain=3.0, q=1.0, enabled=True, band_type=EqBandType.BELL)],
        )
        assert eq.device_name == "EQ1"
        assert len(eq.bands) == 1
        assert eq.bands[0].band_type == EqBandType.BELL


class TestCompressor:
    def test_create_compressor(self):
        comp = Compressor(
            device_name="Comp1",
            device_role="audioFX",
            threshold=-20,
            ratio=4.0,
            attack=0.01,
            release=0.2,
        )
        assert comp.device_name == "Comp1"
        assert comp.threshold.value == -20


class TestMetaData:
    def test_create_metadata(self):
        meta = MetaData(title="My Song", artist="Artist", genre="Rock")
        assert meta.title == "My Song"
        assert meta.artist == "Artist"
        assert meta.genre == "Rock"


class TestArrangement:
    def test_create_arrangement(self):
        arr = Arrangement()
        arr.lanes = Lanes()
        assert arr.lanes is not None
        assert arr.lanes.lanes == []


class TestDoubleAdapter:
    def test_to_xml_normal(self):
        assert DoubleAdapter.to_xml(1.5) == "1.500000"

    def test_to_xml_inf(self):
        assert DoubleAdapter.to_xml(float("inf")) == "inf"

    def test_to_xml_neg_inf(self):
        assert DoubleAdapter.to_xml(float("-inf")) == "-inf"

    def test_to_xml_none(self):
        assert DoubleAdapter.to_xml(None) is None

    def test_from_xml_normal(self):
        assert DoubleAdapter.from_xml("1.5") == 1.5

    def test_from_xml_inf(self):
        assert DoubleAdapter.from_xml("inf") == float("inf")

    def test_from_xml_none(self):
        assert DoubleAdapter.from_xml(None) is None

    def test_from_xml_empty(self):
        assert DoubleAdapter.from_xml("") is None


class TestEnums:
    def test_content_type_values(self):
        assert ContentType.AUDIO.value == "audio"
        assert ContentType.NOTES.value == "notes"
        assert ContentType.AUTOMATION.value == "automation"

    def test_mixer_role_values(self):
        assert MixerRole.MASTER.value == "master"
        assert MixerRole.REGULAR.value == "regular"
        assert MixerRole.EFFECT_TRACK.value == "effect"
        assert MixerRole.SUB_MIX.value == "submix"

    def test_unit_values(self):
        assert Unit.LINEAR.value == "linear"
        assert Unit.BPM.value == "bpm"
        assert Unit.DECIBEL.value == "decibel"

    def test_time_unit_values(self):
        assert TimeUnit.BEATS.value == "beats"
        assert TimeUnit.SECONDS.value == "seconds"

    def test_device_role_values(self):
        assert DeviceRole.AUDIO_FX.value == "audioFX"
        assert DeviceRole.INSTRUMENT.value == "instrument"

    def test_interpolation_values(self):
        assert Interpolation.HOLD.value == "hold"
        assert Interpolation.LINEAR.value == "linear"

    def test_send_type_values(self):
        assert SendType.PRE.value == "pre"
        assert SendType.POST.value == "post"

    def test_eq_band_type_values(self):
        assert EqBandType.BELL.value == "bell"
        assert EqBandType.HIGH_PASS.value == "highPass"

    def test_expression_type_values(self):
        assert ExpressionType.GAIN.value == "gain"
        assert ExpressionType.PAN.value == "pan"
