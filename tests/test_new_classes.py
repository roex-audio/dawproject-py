"""Tests for newly ported classes: plugins, devices, parameters, points, timeline types."""

import pytest
from lxml import etree as ET
from dawproject import (
    Referenceable, RealParameter, BoolParameter, FileReference,
    Unit, TimeUnit, DeviceRole, Interpolation,
    Plugin, Vst2Plugin, Vst3Plugin, ClapPlugin, AuPlugin,
    NoiseGate, Limiter,
    IntegerParameter, EnumParameter,
    BoolPoint, EnumPoint, IntegerPoint, TimeSignaturePoint, RealPoint,
    Video, ClipSlot, Clip, Audio, Notes, Note, Lanes, Clips,
    TimeSignatureParameter, AutomationTarget, ExpressionType,
)


@pytest.fixture(autouse=True)
def reset_ids():
    Referenceable.reset_id()
    yield
    Referenceable.reset_id()


# ---------------------------------------------------------------------------
# Plugin hierarchy
# ---------------------------------------------------------------------------

class TestPlugin:
    def test_vst2_roundtrip(self):
        plugin = Vst2Plugin(
            plugin_version="2.4",
            device_name="MySynth",
            device_id="com.test.mysynth",
        )
        elem = plugin.to_xml()
        assert elem.tag == "Vst2Plugin"
        assert elem.get("pluginVersion") == "2.4"
        assert elem.get("deviceName") == "MySynth"
        assert elem.get("deviceID") == "com.test.mysynth"

        Referenceable.reset_id()
        result = Vst2Plugin.from_xml(elem)
        assert result.plugin_version == "2.4"
        assert result.device_name == "MySynth"
        assert result.device_id == "com.test.mysynth"

    def test_vst3_roundtrip(self):
        plugin = Vst3Plugin(
            plugin_version="3.7",
            device_name="VST3Synth",
        )
        elem = plugin.to_xml()
        assert elem.tag == "Vst3Plugin"
        assert elem.get("pluginVersion") == "3.7"

        Referenceable.reset_id()
        result = Vst3Plugin.from_xml(elem)
        assert result.plugin_version == "3.7"

    def test_clap_roundtrip(self):
        plugin = ClapPlugin(device_name="ClapEffect")
        elem = plugin.to_xml()
        assert elem.tag == "ClapPlugin"

        Referenceable.reset_id()
        result = ClapPlugin.from_xml(elem)
        assert result.device_name == "ClapEffect"

    def test_au_roundtrip(self):
        plugin = AuPlugin(device_name="AUInstrument")
        elem = plugin.to_xml()
        assert elem.tag == "AuPlugin"

        Referenceable.reset_id()
        result = AuPlugin.from_xml(elem)
        assert result.device_name == "AUInstrument"

    def test_plugin_with_state(self):
        plugin = Vst2Plugin(
            device_name="TestPlugin",
            state=FileReference(path="plugins/preset.fxp"),
        )
        elem = plugin.to_xml()
        state_elem = elem.find("State")
        assert state_elem is not None
        assert state_elem.get("path") == "plugins/preset.fxp"

    def test_plugin_with_enabled(self):
        plugin = Vst3Plugin(
            device_name="TestPlugin",
            enabled=BoolParameter(value=True),
        )
        elem = plugin.to_xml()
        enabled_elem = elem.find("Enabled")
        assert enabled_elem is not None
        assert enabled_elem.get("value") == "true"


# ---------------------------------------------------------------------------
# NoiseGate and Limiter
# ---------------------------------------------------------------------------

class TestNoiseGate:
    def test_roundtrip(self):
        ng = NoiseGate(
            device_name="Gate_1",
            threshold=RealParameter(value=-30.0, unit=Unit.DECIBEL),
            ratio=RealParameter(value=4.0, unit=Unit.LINEAR),
            attack=RealParameter(value=0.001, unit=Unit.SECONDS),
            release=RealParameter(value=0.05, unit=Unit.SECONDS),
            range_param=RealParameter(value=-80.0, unit=Unit.DECIBEL),
        )
        elem = ng.to_xml()
        assert elem.tag == "NoiseGate"
        assert elem.get("deviceName") == "Gate_1"
        assert elem.find("Threshold") is not None
        assert elem.find("Ratio") is not None
        assert elem.find("Attack") is not None
        assert elem.find("Release") is not None
        assert elem.find("Range") is not None

        Referenceable.reset_id()
        result = NoiseGate.from_xml(elem)
        assert result.threshold.value == -30.0
        assert result.ratio.value == 4.0
        assert result.range.value == -80.0


class TestLimiter:
    def test_roundtrip(self):
        lim = Limiter(
            device_name="Lim_1",
            threshold=RealParameter(value=-1.0, unit=Unit.DECIBEL),
            input_gain=RealParameter(value=0.0, unit=Unit.DECIBEL),
            output_gain=RealParameter(value=0.0, unit=Unit.DECIBEL),
            attack=RealParameter(value=0.001, unit=Unit.SECONDS),
            release=RealParameter(value=0.1, unit=Unit.SECONDS),
        )
        elem = lim.to_xml()
        assert elem.tag == "Limiter"
        assert elem.find("Threshold") is not None
        assert elem.find("InputGain") is not None
        assert elem.find("OutputGain") is not None

        Referenceable.reset_id()
        result = Limiter.from_xml(elem)
        assert result.threshold.value == -1.0
        assert result.input_gain.value == 0.0
        assert result.output_gain.value == 0.0


# ---------------------------------------------------------------------------
# IntegerParameter, EnumParameter
# ---------------------------------------------------------------------------

class TestIntegerParameter:
    def test_roundtrip(self):
        param = IntegerParameter(value=5, min=0, max=127)
        elem = param.to_xml()
        assert elem.tag == "IntegerParameter"
        assert elem.get("value") == "5"
        assert elem.get("min") == "0"
        assert elem.get("max") == "127"

        Referenceable.reset_id()
        result = IntegerParameter.from_xml(elem)
        assert result.value == 5
        assert result.min == 0
        assert result.max == 127

    def test_none_values(self):
        param = IntegerParameter()
        elem = param.to_xml()
        assert elem.get("value") is None


class TestEnumParameter:
    def test_roundtrip(self):
        param = EnumParameter(value=2, count=4, labels=["Off", "Low", "Med", "High"])
        elem = param.to_xml()
        assert elem.tag == "EnumParameter"
        assert elem.get("value") == "2"
        assert elem.get("count") == "4"
        assert elem.get("labels") == "Off Low Med High"

        Referenceable.reset_id()
        result = EnumParameter.from_xml(elem)
        assert result.value == 2
        assert result.count == 4
        assert result.labels == ["Off", "Low", "Med", "High"]

    def test_empty_labels(self):
        param = EnumParameter(value=0, count=2)
        elem = param.to_xml()
        assert elem.get("labels") is None


# ---------------------------------------------------------------------------
# Point types
# ---------------------------------------------------------------------------

class TestBoolPoint:
    def test_roundtrip(self):
        pt = BoolPoint(time=1.5, value=True)
        elem = pt.to_xml()
        assert elem.tag == "BoolPoint"
        assert elem.get("value") == "true"

        result = BoolPoint.from_xml(elem)
        assert result.value is True
        assert result.time == 1.5

    def test_false_value(self):
        pt = BoolPoint(time=0.0, value=False)
        elem = pt.to_xml()
        assert elem.get("value") == "false"

        result = BoolPoint.from_xml(elem)
        assert result.value is False


class TestEnumPoint:
    def test_roundtrip(self):
        pt = EnumPoint(time=2.0, value=3)
        elem = pt.to_xml()
        assert elem.tag == "EnumPoint"
        assert elem.get("value") == "3"

        result = EnumPoint.from_xml(elem)
        assert result.value == 3
        assert result.time == 2.0


class TestIntegerPoint:
    def test_roundtrip(self):
        pt = IntegerPoint(time=0.5, value=42)
        elem = pt.to_xml()
        assert elem.tag == "IntegerPoint"
        assert elem.get("value") == "42"

        result = IntegerPoint.from_xml(elem)
        assert result.value == 42


class TestTimeSignaturePoint:
    def test_roundtrip(self):
        pt = TimeSignaturePoint(time=0.0, numerator=3, denominator=4)
        elem = pt.to_xml()
        assert elem.tag == "TimeSignaturePoint"
        assert elem.get("numerator") == "3"
        assert elem.get("denominator") == "4"

        result = TimeSignaturePoint.from_xml(elem)
        assert result.numerator == 3
        assert result.denominator == 4
        assert result.time == 0.0


# ---------------------------------------------------------------------------
# Video, ClipSlot
# ---------------------------------------------------------------------------

class TestVideo:
    def test_roundtrip(self):
        video = Video(
            sample_rate=48000,
            channels=2,
            duration=120.5,
            algorithm="stretch",
            file=FileReference(path="video.mp4"),
        )
        elem = video.to_xml()
        assert elem.tag == "Video"
        assert elem.get("sampleRate") == "48000"
        assert elem.get("channels") == "2"
        assert elem.get("algorithm") == "stretch"
        assert elem.find("File").get("path") == "video.mp4"

        Referenceable.reset_id()
        result = Video.from_xml(elem)
        assert result.sample_rate == 48000
        assert result.channels == 2
        assert result.duration == 120.5
        assert result.algorithm == "stretch"
        assert result.file.path == "video.mp4"
        assert result.time_unit == TimeUnit.SECONDS

    def test_defaults(self):
        video = Video()
        assert video.time_unit == TimeUnit.SECONDS


class TestClipSlot:
    def test_roundtrip(self):
        clip = Clip(time=0.0, duration=4.0)
        cs = ClipSlot(has_stop=True, clip=clip)
        elem = cs.to_xml()
        assert elem.tag == "ClipSlot"
        assert elem.get("hasStop") == "true"
        assert elem.find("Clip") is not None

        Referenceable.reset_id()
        result = ClipSlot.from_xml(elem)
        assert result.has_stop is True
        assert result.clip is not None
        assert result.clip.time == 0.0
        assert result.clip.duration == 4.0

    def test_empty_slot(self):
        cs = ClipSlot(has_stop=False)
        elem = cs.to_xml()
        assert elem.get("hasStop") == "false"
        assert elem.find("Clip") is None


# ---------------------------------------------------------------------------
# TimeSignatureParameter (now extends Parameter)
# ---------------------------------------------------------------------------

class TestTimeSignatureParameterExtended:
    def test_has_id(self):
        tsp = TimeSignatureParameter(numerator=4, denominator=4)
        assert hasattr(tsp, "id")
        assert tsp.id.startswith("id")

    def test_roundtrip(self):
        tsp = TimeSignatureParameter(numerator=6, denominator=8)
        elem = tsp.to_xml()
        assert elem.tag == "TimeSignatureParameter"
        assert elem.get("numerator") == "6"
        assert elem.get("denominator") == "8"
        assert elem.get("id") is not None

        Referenceable.reset_id()
        result = TimeSignatureParameter.from_xml(elem)
        assert result.numerator == 6
        assert result.denominator == 8


# ---------------------------------------------------------------------------
# AutomationTarget with ExpressionType enum
# ---------------------------------------------------------------------------

class TestAutomationTargetExpression:
    def test_expression_enum_roundtrip(self):
        target = AutomationTarget(expression=ExpressionType.GAIN)
        elem = target.to_xml()
        assert elem.get("expression") == "gain"

        result = AutomationTarget.from_xml(elem)
        assert result.expression == ExpressionType.GAIN

    def test_idref_roundtrip(self):
        param = RealParameter(value=1.0, unit=Unit.LINEAR)
        target = AutomationTarget(parameter=param)
        elem = target.to_xml()
        assert elem.get("parameter") == param.id

    def test_string_parameter(self):
        target = AutomationTarget(parameter="id42")
        elem = target.to_xml()
        assert elem.get("parameter") == "id42"


# ---------------------------------------------------------------------------
# Timeline super chain tests
# ---------------------------------------------------------------------------

class TestTimelineSuperChain:
    def test_lanes_preserves_id(self):
        lanes = Lanes()
        elem = lanes.to_xml()
        assert elem.get("id") is not None

    def test_clips_preserves_id(self):
        clips = Clips()
        elem = clips.to_xml()
        assert elem.get("id") is not None

    def test_notes_preserves_id(self):
        notes = Notes()
        elem = notes.to_xml()
        assert elem.get("id") is not None

    def test_audio_preserves_id(self):
        audio = Audio(sample_rate=44100, channels=2, duration=5.0)
        elem = audio.to_xml()
        assert elem.get("id") is not None
        assert elem.get("timeUnit") == "seconds"

    def test_lanes_roundtrip_with_id(self):
        lanes = Lanes(time_unit=TimeUnit.BEATS)
        elem = lanes.to_xml()
        original_id = elem.get("id")
        assert original_id is not None

        Referenceable.reset_id()
        result = Lanes.from_xml(elem)
        assert result.id == original_id
        assert result.time_unit == TimeUnit.BEATS

    def test_audio_roundtrip_preserves_all(self):
        audio = Audio(
            sample_rate=48000, channels=1, duration=10.0,
            file=FileReference(path="test.wav"),
            name="TestAudio",
        )
        elem = audio.to_xml()
        assert elem.get("name") == "TestAudio"
        assert elem.get("id") is not None

        Referenceable.reset_id()
        result = Audio.from_xml(elem)
        assert result.name == "TestAudio"
        assert result.sample_rate == 48000
        assert result.channels == 1
        assert result.duration == 10.0
        assert result.file.path == "test.wav"


# ---------------------------------------------------------------------------
# Registry dispatch for new types
# ---------------------------------------------------------------------------

class TestRegistryDispatch:
    def test_resolve_new_point_types(self):
        from dawproject import registry
        registry._TAG_REGISTRY.clear()
        registry._REGISTRY_POPULATED = False
        registry.populate_registry()

        assert registry.resolve_point("BoolPoint") is BoolPoint
        assert registry.resolve_point("EnumPoint") is EnumPoint
        assert registry.resolve_point("IntegerPoint") is IntegerPoint
        assert registry.resolve_point("TimeSignaturePoint") is TimeSignaturePoint

    def test_resolve_new_device_types(self):
        from dawproject import registry
        registry._TAG_REGISTRY.clear()
        registry._REGISTRY_POPULATED = False
        registry.populate_registry()

        assert registry.resolve_device("Vst2Plugin") is Vst2Plugin
        assert registry.resolve_device("Vst3Plugin") is Vst3Plugin
        assert registry.resolve_device("ClapPlugin") is ClapPlugin
        assert registry.resolve_device("AuPlugin") is AuPlugin
        assert registry.resolve_device("NoiseGate") is NoiseGate
        assert registry.resolve_device("Limiter") is Limiter

    def test_resolve_new_timeline_types(self):
        from dawproject import registry
        registry._TAG_REGISTRY.clear()
        registry._REGISTRY_POPULATED = False
        registry.populate_registry()

        assert registry.resolve_timeline("Video") is Video
        assert registry.resolve_timeline("ClipSlot") is ClipSlot

    def test_resolve_lowercase_markers(self):
        """XSD global element is <markers> (lowercase); registry must handle both cases."""
        from dawproject.markers import Markers
        from dawproject import registry
        registry._TAG_REGISTRY.clear()
        registry._REGISTRY_POPULATED = False
        registry.populate_registry()

        assert registry.resolve_timeline("Markers") is Markers
        assert registry.resolve_timeline("markers") is Markers

    def test_resolve_timeline_rejects_non_timeline(self):
        """resolve_timeline must return None for registered non-Timeline types."""
        from dawproject import registry
        registry._TAG_REGISTRY.clear()
        registry._REGISTRY_POPULATED = False
        registry.populate_registry()

        # Compressor is a Device, not a Timeline
        assert registry.resolve_timeline("Compressor") is None
        # RealParameter is a Parameter, not a Timeline
        assert registry.resolve_timeline("RealParameter") is None
        # BoolPoint is a Point, not a Timeline
        assert registry.resolve_timeline("BoolPoint") is None

    def test_resolve_device_rejects_non_device(self):
        """resolve_device must return None for registered non-Device types."""
        from dawproject import registry
        registry._TAG_REGISTRY.clear()
        registry._REGISTRY_POPULATED = False
        registry.populate_registry()

        # Clips is a Timeline, not a Device
        assert registry.resolve_device("Clips") is None
        # RealPoint is a Point, not a Device
        assert registry.resolve_device("RealPoint") is None
        # BoolParameter is a Parameter, not a Device
        assert registry.resolve_device("BoolParameter") is None

    def test_resolve_point_rejects_non_point(self):
        """resolve_point must return None for registered non-Point types."""
        from dawproject import registry
        registry._TAG_REGISTRY.clear()
        registry._REGISTRY_POPULATED = False
        registry.populate_registry()

        # Lanes is a Timeline, not a Point
        assert registry.resolve_point("Lanes") is None
        # Compressor is a Device, not a Point
        assert registry.resolve_point("Compressor") is None
        # IntegerParameter is a Parameter, not a Point
        assert registry.resolve_point("IntegerParameter") is None

    def test_resolve_parameter_rejects_non_parameter(self):
        """resolve_parameter must return None for registered non-Parameter types."""
        from dawproject import registry
        registry._TAG_REGISTRY.clear()
        registry._REGISTRY_POPULATED = False
        registry.populate_registry()

        # Notes is a Timeline, not a Parameter
        assert registry.resolve_parameter("Notes") is None
        # Plugin is a Device, not a Parameter
        assert registry.resolve_parameter("Plugin") is None
        # RealPoint is a Point, not a Parameter
        assert registry.resolve_parameter("RealPoint") is None

    def test_resolve_unknown_tag_returns_none(self):
        """All resolve_* functions return None for unregistered tag names."""
        from dawproject import registry
        registry._TAG_REGISTRY.clear()
        registry._REGISTRY_POPULATED = False
        registry.populate_registry()

        assert registry.resolve_timeline("NonExistent") is None
        assert registry.resolve_point("NonExistent") is None
        assert registry.resolve_parameter("NonExistent") is None
        assert registry.resolve_device("NonExistent") is None
