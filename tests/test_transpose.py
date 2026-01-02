import pretty_midi
from app.services.transformation_service import MidiTransformationService


def test_transpose_increases_pitch_by_semitones(simple_midi_file):
    service = MidiTransformationService()

    semitones = 3
    result = service.transpose(simple_midi_file, semitones)

    output_path = result["output_path"]
    transformed = pretty_midi.PrettyMIDI(output_path)

    original = pretty_midi.PrettyMIDI(simple_midi_file)

    original_pitches = [
        note.pitch
        for instr in original.instruments
        for note in instr.notes
    ]

    transformed_pitches = [
        note.pitch
        for instr in transformed.instruments
        for note in instr.notes
    ]

    for orig, trans in zip(original_pitches, transformed_pitches):
        assert trans == orig + semitones
