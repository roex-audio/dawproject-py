"""Tests for XML deserialization (from_xml) of DAWproject models."""

import pytest
from lxml import etree as ET
from dawproject import (
    Project, Application, Transport, Track, Channel,
    Arrangement, Lanes, Clips, Clip, Audio, Notes, Note,
    Markers, Marker, Points, RealPoint, Send,
    RealParameter, BoolParameter, TimeSignatureParameter,
    Equalizer, Compressor, EqBand, MetaData,
    ContentType, MixerRole, TimeUnit, Unit, DeviceRole,
    EqBandType, Interpolation, SendType,
    Referenceable, FileReference,
)


@pytest.fixture(autouse=True)
def reset_ids():
    Referenceable.reset_id()
    yield
    Referenceable.reset_id()


class TestProjectDeserialization:
    def test_parse_minimal_project(self):
        xml = '<Project version="1.0"><Application name="Test" version="1.0"/></Project>'
        root = ET.fromstring(xml)
        project = Project.from_xml(root)

        assert project.version == "1.0"
        assert project.application.name == "Test"
        assert project.structure == []

    def test_parse_project_with_structure(self):
        xml = """
        <Project version="1.0">
            <Application name="Test" version="1.0"/>
            <Structure>
                <Track name="Master" id="id0" loaded="true">
                    <Channel id="id1" role="master" audioChannels="2"/>
                </Track>
                <Track name="Bass" id="id2" contentType="audio" loaded="true">
                    <Channel id="id3" role="regular" audioChannels="2" destination="id1"/>
                </Track>
            </Structure>
        </Project>
        """
        root = ET.fromstring(xml)
        project = Project.from_xml(root)

        assert len(project.structure) == 2
        assert project.structure[0].name == "Master"
        assert project.structure[1].name == "Bass"
        assert project.structure[1].channel is not None
        assert project.structure[1].channel.role == MixerRole.REGULAR
        assert project.structure[1].content_type == [ContentType.AUDIO]


class TestTrackDeserialization:
    def test_parse_track(self):
        xml = '<Track name="Vocals" id="id0" contentType="audio notes" loaded="true"/>'
        elem = ET.fromstring(xml)
        track = Track.from_xml(elem)

        assert track.name == "Vocals"
        assert track.loaded is True
        assert ContentType.AUDIO in track.content_type
        assert ContentType.NOTES in track.content_type

    def test_parse_track_with_channel(self):
        xml = """
        <Track name="Lead" id="id0">
            <Channel id="id1" role="regular" audioChannels="2">
                <Volume id="id2" value="0.8" unit="linear"/>
                <Pan id="id3" value="0.5" unit="normalized"/>
            </Channel>
        </Track>
        """
        elem = ET.fromstring(xml)
        track = Track.from_xml(elem)

        assert track.channel is not None
        assert track.channel.volume.value == 0.8
        assert track.channel.volume.unit == Unit.LINEAR
        assert track.channel.pan.value == 0.5


class TestChannelDeserialization:
    def test_parse_channel_role(self):
        xml = '<Channel id="id0" role="master" audioChannels="2"/>'
        elem = ET.fromstring(xml)
        ch = Channel.from_xml(elem)

        assert ch.role == MixerRole.MASTER
        assert ch.audio_channels == 2


class TestRealParameterDeserialization:
    def test_parse_real_parameter(self):
        xml = '<RealParameter id="id0" value="0.75" unit="linear" min="0.0" max="1.0"/>'
        elem = ET.fromstring(xml)
        param = RealParameter.from_xml(elem)

        assert param.value == 0.75
        assert param.unit == Unit.LINEAR
        assert param.min == 0.0
        assert param.max == 1.0

    def test_parse_bpm_parameter(self):
        xml = '<Tempo id="id0" value="120.0" unit="bpm"/>'
        elem = ET.fromstring(xml)
        param = RealParameter.from_xml(elem)

        assert param.value == 120.0
        assert param.unit == Unit.BPM


class TestClipDeserialization:
    def test_parse_clip_with_audio(self):
        xml = """
        <Clip time="0" duration="10.0">
            <Audio duration="10.0" sampleRate="44100" channels="2" timeUnit="seconds">
                <File path="test.wav" external="false"/>
            </Audio>
        </Clip>
        """
        elem = ET.fromstring(xml)
        clip = Clip.from_xml(elem)

        assert clip.time == 0.0
        assert clip.duration == 10.0
        assert isinstance(clip.content, Audio)
        assert clip.content.sample_rate == 44100
        assert clip.content.file.path == "test.wav"


class TestAudioDeserialization:
    def test_parse_audio(self):
        xml = """
        <Audio duration="5.0" sampleRate="48000" channels="1" timeUnit="seconds">
            <File path="vocal.wav" external="true"/>
        </Audio>
        """
        elem = ET.fromstring(xml)
        audio = Audio.from_xml(elem)

        assert audio.sample_rate == 48000
        assert audio.channels == 1
        assert audio.duration == 5.0
        assert audio.time_unit == TimeUnit.SECONDS
        assert audio.file.path == "vocal.wav"
        assert audio.file.external is True


class TestLanesDeserialization:
    def test_parse_lanes_with_clips(self):
        xml = """
        <Lanes timeUnit="seconds">
            <Clips track="id0">
                <Clip time="0" duration="5.0"/>
            </Clips>
        </Lanes>
        """
        elem = ET.fromstring(xml)
        lanes = Lanes.from_xml(elem)

        assert lanes.time_unit == TimeUnit.SECONDS
        assert len(lanes.lanes) == 1
        assert isinstance(lanes.lanes[0], Clips)


class TestNotesDeserialization:
    def test_parse_notes(self):
        xml = """
        <Notes>
            <Note time="0.0" duration="1.0" key="60" vel="100.0"/>
            <Note time="1.0" duration="0.5" key="64" vel="80.0"/>
        </Notes>
        """
        elem = ET.fromstring(xml)
        notes = Notes.from_xml(elem)

        assert len(notes.notes) == 2
        assert notes.notes[0].key == 60
        assert notes.notes[0].vel == 100.0
        assert notes.notes[1].key == 64


class TestMarkersDeserialization:
    def test_parse_markers(self):
        xml = """
        <Markers>
            <Marker time="0.0" name="Intro"/>
            <Marker time="32.0" name="Verse"/>
        </Markers>
        """
        elem = ET.fromstring(xml)
        markers = Markers.from_xml(elem)

        assert len(markers.markers) == 2
        assert markers.markers[0].name == "Intro"
        assert markers.markers[1].time == 32.0


class TestEqualizerDeserialization:
    def test_parse_equalizer(self):
        xml = """
        <Equalizer deviceName="EQ_1" deviceRole="audioFX">
            <Band type="bell">
                <Freq id="id0" value="1000" unit="hertz"/>
                <Gain id="id1" value="3.0" unit="decibel"/>
                <Q id="id2" value="1.0" unit="linear"/>
                <Enabled id="id3" value="true"/>
            </Band>
            <InputGain id="id4" value="0.0" unit="decibel"/>
            <OutputGain id="id5" value="0.0" unit="decibel"/>
        </Equalizer>
        """
        elem = ET.fromstring(xml)
        eq = Equalizer.from_xml(elem)

        assert eq.device_name == "EQ_1"
        assert len(eq.bands) == 1
        assert eq.bands[0].band_type == EqBandType.BELL
        assert eq.input_gain.value == 0.0


class TestMetaDataDeserialization:
    def test_parse_metadata(self):
        xml = """
        <MetaData>
            <Title>My Song</Title>
            <Artist>Test Artist</Artist>
            <Year>2025</Year>
        </MetaData>
        """
        elem = ET.fromstring(xml)
        meta = MetaData.from_xml(elem)

        assert meta.title == "My Song"
        assert meta.artist == "Test Artist"
        assert meta.year == "2025"
        assert meta.album is None
