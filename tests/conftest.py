import pytest
import pretty_midi


@pytest.fixture
def simple_midi_file(tmp_path):
    """
    Creates a simple MIDI file with known pitches and duration.
    Returns the file path.
    """

    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)

    # Known pitches: C4, D4, E4
    notes = [
        pretty_midi.Note(velocity=100, pitch=60, start=0.0, end=1.0),
        pretty_midi.Note(velocity=100, pitch=62, start=1.0, end=2.0),
        pretty_midi.Note(velocity=100, pitch=64, start=2.0, end=3.0),
    ]

    instrument.notes.extend(notes)
    midi.instruments.append(instrument)

    path = tmp_path / "simple.mid"
    midi.write(str(path))

    return str(path)
