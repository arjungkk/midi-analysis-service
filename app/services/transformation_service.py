import time
import os
from uuid import uuid4
import pretty_midi


class MidiTransformationService:

    def __init__(self, output_path="data/outputs"):
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)

    def transpose(self, source_path: str, semitones: int) -> dict:
        start = time.time()

        midi = pretty_midi.PrettyMIDI(source_path)

        for instrument in midi.instruments:
            for note in instrument.notes:
                note.pitch = max(0, min(127, note.pitch + semitones))

        output_file = self._save_output(midi)

        return {
            "output_path": output_file,
            "processing_time_ms": int((time.time() - start) * 1000)
        }

    def change_tempo(self, source_path: str, tempo_multiplier: float) -> dict:
        start = time.time()

        midi = pretty_midi.PrettyMIDI(source_path)

        for instrument in midi.instruments:
            for note in instrument.notes:
                note.start *= tempo_multiplier
                note.end *= tempo_multiplier

        output_file = self._save_output(midi)

        return {
            "output_path": output_file,
            "processing_time_ms": int((time.time() - start) * 1000)
        }

    def _save_output(self, midi: pretty_midi.PrettyMIDI) -> str:
        filename = f"{uuid4()}.mid"
        path = os.path.join(self.output_path, filename)
        midi.write(path)
        return path
