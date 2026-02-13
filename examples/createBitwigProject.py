import os
from dawproject.referenceable import Referenceable
from dawproject.project import Project
from dawproject.application import Application
from dawproject.realParameter import RealParameter
from dawproject.mixerRole import MixerRole
from dawproject.deviceRole import DeviceRole
from dawproject.arrangement import Arrangement
from dawproject.lanes import Lanes
from dawproject.timeUnit import TimeUnit
from dawproject.dawProject import DawProject
from dawproject.metaData import MetaData
from dawproject.utility import Utility
from dawproject.contentType import ContentType
from dawproject.transport import Transport
from dawproject.unit import Unit
from dawproject.compressor import Compressor
from dawproject.equalizer import Equalizer
from dawproject.eqBand import EqBand
from dawproject.eqBandType import EqBandType


def create_empty_project():
    Referenceable.reset_id()
    project = Project()
    project.application = Application(name="RoEx Automix", version="1.0")
    return project


def get_audio_file_as_bytes(sample_path):
    """
    Method to retrieve the audio file content as bytes.
    """
    with open(sample_path, 'rb') as audio_file:
        return audio_file.read()


def save_test_project(project, name, configurer=None):
    metadata = MetaData()
    embedded_files = {}

    if configurer:
        configurer(metadata, embedded_files)

    DawProject.save(project, metadata, embedded_files, f"../target/{name}.dawproject")
    DawProject.save_xml(project, f"../target/{name}.xml")
    DawProject.validate(project)


def create_project_with_audio_tracks(audio_tracks):
    """
    Create a DAW project with the provided audio tracks, each with its gain, panning, EQ, and compressor settings.

    :param audio_tracks: List of dictionaries where each dictionary contains the following keys:
        - 'file_path': The location of the audio file.
        - 'gain': The gain setting for the track (in dB).
        - 'pan': The panning setting for the track (range -1.0 to 1.0).
        - 'eq_settings': List of dictionaries with EQ band settings. Each dictionary should contain:
            - 'frequency': The frequency of the EQ band (in Hz).
            - 'gain': The gain for the EQ band (in dB).
            - 'q': The Q factor for the EQ band.
            - 'enabled': Boolean to enable/disable the EQ band.
            - 'band_type': Type of EQ band (e.g., 'bell', 'high_shelf', etc.).
        - 'compressor_settings': Dictionary with compressor settings:
            - 'threshold': Threshold (in dB).
            - 'ratio': Compression ratio.
            - 'attack': Attack time (in seconds).
            - 'release': Release time (in seconds).
            - 'input_gain': Input gain (in dB).
            - 'output_gain': Output gain (in dB).
            - 'auto_makeup': Boolean to enable/disable automatic makeup gain.
    """
    project = create_empty_project()
    project.transport = Transport()
    project.transport.tempo = RealParameter()
    project.transport.tempo.unit = Unit.BPM
    project.transport.tempo.value = 120.0

    master_track = Utility.create_track(name="Master", content_types=set(), mixer_role=MixerRole.MASTER, pan=0.5,
                                        volume=1.0)
    project.structure.append(master_track)
    project.arrangement = Arrangement()
    project.arrangement.lanes = Lanes()
    project.arrangement.lanes.time_unit = TimeUnit.SECONDS

    embedded_files = {}

    for i, track_info in enumerate(audio_tracks):
        # Create audio track
        track_name = os.path.basename(track_info['file_path'])
        audio_track = Utility.create_track(name=track_name, content_types={ContentType.AUDIO},
                                           mixer_role=MixerRole.REGULAR, pan=track_info['pan'],
                                           volume=track_info['gain'])
        audio_track.channel.destination = master_track.channel
        project.structure.append(audio_track)

        # Load audio file
        sample_path = track_info['file_path']
        sample_duration = track_info['sample_duration']  # Assuming this method exists to determine duration
        audio = Utility.create_audio(track_name, 44100, 2, sample_duration)
        audio.file.external = True
        audio.file.path = os.path.abspath(sample_path)

        # Add the audio file to the embedded files
        embedded_files[get_audio_file_as_bytes(os.path.abspath(sample_path))] = os.path.basename(sample_path)

        # Create and add clip to the track
        audio_clip = Utility.create_clip(audio, 0, sample_duration)
        audio_clip.content_time_unit = TimeUnit.SECONDS
        audio_clip.play_start = 0

        clips = Utility.create_clips(audio_clip)
        clips.track = audio_track

        # Create lanes and add clips to arrangement
        project.arrangement.lanes.lanes.append(clips)

        # Apply EQ settings
        if 'eq_settings' in track_info:
            eq_bands = []
            for eq_band_info in track_info['eq_settings']:
                eq_band = EqBand(
                    freq=eq_band_info['frequency'],
                    gain=eq_band_info['gain'],
                    q=eq_band_info['q'],
                    enabled=eq_band_info['enabled'],
                    band_type=EqBandType[eq_band_info['band_type'].upper()]
                )
                eq_bands.append(eq_band)
            equalizer = Equalizer(device_name=f"Eq_{i + 1}", device_role=DeviceRole.AUDIO_FX.value, bands=eq_bands)
            audio_track.channel.devices.append(equalizer)

        # Apply Compressor settings
        if 'compressor_settings' in track_info:
            comp_info = track_info['compressor_settings']
            compressor = Compressor(
                device_name=f"Compressor_{i + 1}",
                device_role=DeviceRole.AUDIO_FX.value,
                threshold=comp_info['threshold'],
                ratio=comp_info['ratio'],
                attack=comp_info['attack'],
                release=comp_info['release'],
                input_gain=comp_info['input_gain'],
                output_gain=comp_info['output_gain'],
                auto_makeup=comp_info['auto_makeup']
            )
            audio_track.channel.devices.append(compressor)

    # Save the project once after all tracks are added
    save_test_project(project, "RoEx_Automix", lambda meta, files: files.update(embedded_files))


if __name__ == "__main__":

    # Example usage
    audio_tracks = [
        {
            'file_path': './audio_in/masks-bass.wav',
            'sample_duration': 30,
            'gain': 0.7,
            'pan': 0.5,
            'eq_settings': [
                {'frequency': 100, 'gain': 6, 'q': 1.0, 'enabled': True, 'band_type': 'bell'},
                {'frequency': 1000, 'gain': -3, 'q': 1.0, 'enabled': True, 'band_type': 'high_shelf'}
            ],
            'compressor_settings': {
                'threshold': -15,
                'ratio': 0.5,
                'attack': 0.01,
                'release': 0.2,
                'input_gain': 0.0,
                'output_gain': 0.0,
                'auto_makeup': True
            }
        },
        {
            'file_path': './audio_in/masks-chord.wav',
            'sample_duration': 30,
            'gain': 0.9,
            'pan': 0.7,
            'eq_settings': [
                {'frequency': 100, 'gain': 6, 'q': 1.0, 'enabled': True, 'band_type': 'bell'},
                {'frequency': 1000, 'gain': -3, 'q': 1.0, 'enabled': True, 'band_type': 'high_shelf'}
            ],
            'compressor_settings': {
                'threshold': -15,
                'ratio': 0.5,
                'attack': 0.01,
                'release': 0.2,
                'input_gain': 0.0,
                'output_gain': 0.0,
                'auto_makeup': True
            }
        },
        {
            'file_path': './audio_in/masks-kick.wav',
            'sample_duration': 30,
            'gain': 0.2,
            'pan': 0.5,
            'eq_settings': [
                {'frequency': 100, 'gain': 6, 'q': 1.0, 'enabled': True, 'band_type': 'bell'},
                {'frequency': 1000, 'gain': -3, 'q': 1.0, 'enabled': True, 'band_type': 'high_shelf'}
            ],
            'compressor_settings': {
                'threshold': -15,
                'ratio': 0.3,
                'attack': 0.01,
                'release': 0.2,
                'input_gain': 0.0,
                'output_gain': 0.0,
                'auto_makeup': True
            }
        },
        {
            'file_path': './audio_in/masks-percussion.wav',
            'sample_duration': 30,
            'gain': 0.7,
            'pan': 0.5,
            'eq_settings': [
                {'frequency': 100, 'gain': 6, 'q': 1.0, 'enabled': True, 'band_type': 'bell'},
                {'frequency': 1000, 'gain': -3, 'q': 1.0, 'enabled': True, 'band_type': 'high_shelf'}
            ],
            'compressor_settings': {
                'threshold': -5,
                'ratio': 0.2,
                'attack': 0.01,
                'release': 0.2,
                'input_gain': 0.0,
                'output_gain': 0.0,
                'auto_makeup': True
            }
        },
        {
            'file_path': './audio_in/masks-synth.wav',
            'sample_duration': 30,
            'gain': 0.4,
            'pan': 0.2,
            'eq_settings': [
                {'frequency': 100, 'gain': 6, 'q': 1.0, 'enabled': True, 'band_type': 'bell'},
                {'frequency': 1000, 'gain': -3, 'q': 1.0, 'enabled': True, 'band_type': 'high_shelf'}
            ],
            'compressor_settings': {
                'threshold': -35,
                'ratio': 0.7,
                'attack': 0.01,
                'release': 0.2,
                'input_gain': 0.0,
                'output_gain': 0.0,
                'auto_makeup': True
            }
        },
        # Add more tracks here
    ]

    # Create the DAW project with the specified audio tracks
    create_project_with_audio_tracks(audio_tracks)
