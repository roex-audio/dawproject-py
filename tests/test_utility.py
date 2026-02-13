"""Tests for the Utility factory class."""

import pytest
from dawproject import (
    Utility, Track, Channel, Audio, Clip, Clips, Warp,
    RealParameter, ContentType, MixerRole, TimeUnit, Unit,
    Referenceable, FileReference,
)


@pytest.fixture(autouse=True)
def reset_ids():
    Referenceable.reset_id()
    yield
    Referenceable.reset_id()


class TestCreateTrack:
    def test_creates_track_with_channel(self):
        track = Utility.create_track("Bass", {ContentType.AUDIO}, MixerRole.REGULAR, 0.8, 0.5)

        assert isinstance(track, Track)
        assert track.name == "Bass"
        assert track.loaded is True
        assert ContentType.AUDIO in track.content_type

        assert track.channel is not None
        assert isinstance(track.channel, Channel)
        assert track.channel.role == MixerRole.REGULAR
        assert track.channel.volume.value == 0.8
        assert track.channel.volume.unit == Unit.LINEAR
        assert track.channel.pan.value == 0.5
        assert track.channel.pan.unit == Unit.NORMALIZED

    def test_master_track(self):
        track = Utility.create_track("Master", set(), MixerRole.MASTER, 1.0, 0.5)

        assert track.name == "Master"
        assert track.channel.role == MixerRole.MASTER
        assert len(track.content_type) == 0


class TestCreateAudio:
    def test_creates_audio(self):
        audio = Utility.create_audio("vocals.wav", 48000, 1, 30.0)

        assert isinstance(audio, Audio)
        assert audio.file.path == "vocals.wav"
        assert audio.file.external is False
        assert audio.sample_rate == 48000
        assert audio.channels == 1
        assert audio.duration == 30.0
        assert audio.time_unit == TimeUnit.SECONDS


class TestCreateWarp:
    def test_creates_warp(self):
        warp = Utility.create_warp(1.0, 2.0)

        assert isinstance(warp, Warp)
        assert warp.time == 1.0
        assert warp.content_time == 2.0


class TestCreateClip:
    def test_creates_clip(self):
        audio = Utility.create_audio("test.wav", 44100, 2, 5.0)
        clip = Utility.create_clip(audio, 0, 5.0)

        assert isinstance(clip, Clip)
        assert clip.time == 0
        assert clip.duration == 5.0
        assert clip.content is audio


class TestCreateClips:
    def test_creates_clips_container(self):
        audio1 = Utility.create_audio("a.wav", 44100, 2, 5.0)
        audio2 = Utility.create_audio("b.wav", 44100, 2, 3.0)
        clip1 = Utility.create_clip(audio1, 0, 5.0)
        clip2 = Utility.create_clip(audio2, 5.0, 3.0)
        clips = Utility.create_clips(clip1, clip2)

        assert isinstance(clips, Clips)
        assert len(clips.clips) == 2
        assert clips.clips[0] is clip1
        assert clips.clips[1] is clip2
