import time
import pretty_midi
from uuid import uuid4
import os


class MidiTransformationService:

    def __init__(self, output_dir="data/outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def transpose(self, input_path: str, semitones: int) -> dict:
        start = time.time()

        midi = pretty_midi.PrettyMIDI(input_path)

        for instrument in midi.instruments:
            for note in instrument.notes:
                note.pitch = max(0, min(127, note.pitch + semitones))

        output_path = self._save_output(midi)

        return self._result(output_path, start)

    def change_tempo(self, input_path: str, factor: float) -> dict:
        start = time.time()

        midi = pretty_midi.PrettyMIDI(input_path)

        original_end = midi.get_end_time()
        midi.adjust_times(
            [0, original_end],
            [0, original_end / factor]
        )

        output_path = self._save_output(midi)

        return self._result(output_path, start)

    def _save_output(self, midi):
        filename = f"{uuid4()}.mid"
        path = os.path.join(self.output_dir, filename)
        midi.write(path)
        return path

    def _result(self, output_path, start_time):
        return {
            "output_path": output_path,
            "processing_time_ms": int((time.time() - start_time) * 1000)
        }
