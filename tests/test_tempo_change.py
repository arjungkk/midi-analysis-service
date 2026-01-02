import pretty_midi
from app.services.transformation_service import MidiTransformationService


def test_tempo_change_scales_duration(simple_midi_file):
    service = MidiTransformationService()

    factor = 2.0  # 2x faster
    result = service.change_tempo(simple_midi_file, factor)

    output_path = result["output_path"]

    original = pretty_midi.PrettyMIDI(simple_midi_file)
    transformed = pretty_midi.PrettyMIDI(output_path)

    original_duration = original.get_end_time()
    transformed_duration = transformed.get_end_time()

    expected_duration = original_duration / factor

    assert abs(transformed_duration - expected_duration) < 0.01
