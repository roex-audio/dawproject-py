# DAWProject-Py

*Python library for working with DAWProject files — enabling DAW interoperability.*

[![License](https://img.shields.io/github/license/roex-audio/dawproject-py)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/roex-audio/dawproject-py.svg)](https://github.com/roex-audio/dawproject-py/stargazers)

## About

DAWProject is an **open XML-based file format** designed for **seamless project exchange between DAWs**. It allows music producers, engineers, and developers to share full session data between different DAWs without losing important information.

The original **DAWProject** repository, developed by **Bitwig**, was written in **Java**. At **RoEx**, we primarily develop in **Python and C++**, so we converted the core classes to Python to integrate with our systems and allow more developers to build upon it.

We love the idea of DAWProject and want to see it in every DAW. The more people building on it, the better — so we're making our Python version publicly available. If anyone wants to extend it or modify it further, feel free!

For reference, we've kept the original Java classes and implementations for posterity.

---

## Installation

### From source

```sh
git clone https://github.com/roex-audio/dawproject-py.git
cd dawproject-py
pip install -e .
```

### Dependencies

- `lxml` (XML parsing and generation)
- `chardet` (character encoding detection)

---

## Quick Start

### Loading a DAWProject file

```python
from dawproject import DawProject, Referenceable

# Reset ID registry before loading
Referenceable.reset_id()

# Load a .dawproject file
project = DawProject.load_project("example.dawproject")

# Inspect project
print(f"Application: {project.application.name} {project.application.version}")
print(f"Tracks: {len(project.structure)}")

for track in project.structure:
    print(f"  - {track.name}")
    if track.channel:
        print(f"    Volume: {track.channel.volume.value if track.channel.volume else 'N/A'}")

# Load metadata
metadata = DawProject.load_metadata("example.dawproject")
print(f"Title: {metadata.title}")
print(f"Artist: {metadata.artist}")
```

### Creating an Empty DAWProject

```python
from dawproject import Project, Application, DawProject

# Initialize an empty project
project = Project()
project.application = Application(name="My App", version="1.0")

# Save as standalone XML
DawProject.save_xml(project, "new_project.xml")
```

### Creating a Project with Audio Tracks

```python
from dawproject import (
    Project, Application, DawProject, MetaData,
    Utility, MixerRole, ContentType, TimeUnit,
    Arrangement, Lanes, Referenceable,
)

Referenceable.reset_id()

# Create project with transport
project = Project()
project.application = Application(name="My App", version="1.0")

# Create a master track
master = Utility.create_track(
    name="Master",
    content_types=set(),
    mixer_role=MixerRole.MASTER,
    volume=1.0,
    pan=0.5,
)
project.structure.append(master)

# Create an audio track routed to master
audio_track = Utility.create_track(
    name="Lead Synth",
    content_types={ContentType.AUDIO},
    mixer_role=MixerRole.REGULAR,
    volume=0.8,
    pan=0.5,
)
audio_track.channel.destination = master.channel
project.structure.append(audio_track)

# Create audio content and add to arrangement
audio = Utility.create_audio("lead.wav", sample_rate=44100, channels=2, duration=30.0)
clip = Utility.create_clip(audio, time=0, duration=30.0)
clips = Utility.create_clips(clip)
clips.track = audio_track

project.arrangement = Arrangement()
project.arrangement.lanes = Lanes()
project.arrangement.lanes.time_unit = TimeUnit.SECONDS
project.arrangement.lanes.lanes.append(clips)

# Save as .dawproject (ZIP archive)
metadata = MetaData(title="My Song", artist="My Name")
DawProject.save(project, metadata, {}, "my_project.dawproject")

# Or save as standalone XML
DawProject.save_xml(project, "my_project.xml")
```

### Adding EQ and Compressor

```python
from dawproject import Equalizer, Compressor, EqBand, EqBandType, DeviceRole

# Add an equalizer to a track
eq = Equalizer(
    device_name="Track EQ",
    device_role=DeviceRole.AUDIO_FX.value,
    bands=[
        EqBand(freq=100, gain=3.0, q=1.0, enabled=True, band_type=EqBandType.BELL),
        EqBand(freq=5000, gain=-2.0, q=0.8, enabled=True, band_type=EqBandType.HIGH_SHELF),
    ],
)
audio_track.channel.devices.append(eq)

# Add a compressor
comp = Compressor(
    device_name="Track Comp",
    device_role=DeviceRole.AUDIO_FX.value,
    threshold=-20,
    ratio=4.0,
    attack=0.01,
    release=0.2,
    input_gain=0.0,
    output_gain=0.0,
    auto_makeup=True,
)
audio_track.channel.devices.append(comp)
```

---

## API Reference

### DawProject (main entry point)

| Method | Description |
|--------|-------------|
| `DawProject.save_xml(project, file)` | Save a Project as standalone XML |
| `DawProject.save(project, metadata, embedded_files, file)` | Save a full .dawproject ZIP archive |
| `DawProject.load_project(file)` | Load a Project from a .dawproject file |
| `DawProject.load(file)` | Alias for `load_project` |
| `DawProject.load_metadata(file)` | Load MetaData from a .dawproject file |
| `DawProject.validate(project)` | Validate a Project against the XSD schema |
| `DawProject.stream_embedded(file, path)` | Read an embedded file from the archive |

### Utility (factory methods)

| Method | Description |
|--------|-------------|
| `Utility.create_track(name, content_types, mixer_role, volume, pan)` | Create a Track with Channel |
| `Utility.create_audio(path, sample_rate, channels, duration)` | Create an Audio timeline |
| `Utility.create_clip(content, time, duration)` | Create a Clip |
| `Utility.create_clips(*clips)` | Create a Clips container |
| `Utility.create_warp(time, content_time)` | Create a Warp point |

### Core Models

| Class | Description |
|-------|-------------|
| `Project` | Top-level container (version, application, structure, arrangement) |
| `Track` | A track with channel, content type, nested tracks |
| `Channel` | Mixer channel (volume, pan, sends, devices) |
| `Clip` | A clip on a timeline with content |
| `Audio` | Audio file reference with sample rate, channels, duration |
| `Notes` / `Note` | MIDI note data |
| `Markers` / `Marker` | Named timeline markers |
| `Points` / `RealPoint` | Automation data |
| `Lanes` / `Clips` | Timeline containers |

### Enums

| Enum | Values |
|------|--------|
| `ContentType` | AUDIO, NOTES, AUTOMATION, VIDEO, MARKERS, TRACKS |
| `MixerRole` | REGULAR, MASTER, EFFECT_TRACK, SUB_MIX, VCA |
| `Unit` | LINEAR, NORMALIZED, PERCENT, DECIBEL, HERTZ, SEMITONES, SECONDS, BEATS, BPM |
| `TimeUnit` | BEATS, SECONDS |
| `DeviceRole` | INSTRUMENT, NOTE_FX, AUDIO_FX, ANALYZER |
| `SendType` | PRE, POST |
| `EqBandType` | HIGH_PASS, LOW_PASS, BAND_PASS, HIGH_SHELF, LOW_SHELF, BELL, NOTCH |
| `Interpolation` | HOLD, LINEAR |

---

## Examples

An `examples/` folder is included demonstrating how to use DAWProject-Py in real-world scenarios:

- **`createBitwigProject.py`** — Creates a project with audio tracks, EQ, and compressor settings
- **`roex_daw_project_export.py`** — Uses the Tonn API to obtain multitrack mix settings and create a DAWProject file

---

## DAWProject Format

DAWProject is an open XML-based format designed to enable cross-DAW compatibility. Instead of exporting audio stems, `.dawproject` files allow projects to be shared across DAWs while preserving:

- Track names, volume, and panning
- Effects and automation data
- MIDI and audio region placements
- Tempo and time signature changes

For the full specification, visit [DAWProject on GitHub](https://github.com/bitwig/dawproject).

---

## Development

### Setup

```sh
git clone https://github.com/roex-audio/dawproject-py.git
cd dawproject-py
pip install -e ".[dev]"
```

### Running Tests

```sh
pytest
```

### Contributing

- Fork the repository
- Create a feature branch (`git checkout -b feature-name`)
- Commit your changes (`git commit -m "Add feature XYZ"`)
- Push to GitHub (`git push origin feature-name`)
- Open a Pull Request

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Stay Connected

- **Website:** [www.roexaudio.com](https://www.roexaudio.com)
- **GitHub Discussions:** [DAWProject-Py Discussions](https://github.com/roex-audio/dawproject-py/discussions)
