import pretty_midi
import numpy as np


class MidiAnalysisService:

    def analyze(self, file_path: str) -> dict:
        midi = pretty_midi.PrettyMIDI(file_path)

        duration = midi.get_end_time()
        tempo = self._estimate_tempo(midi)
        time_signature = self._extract_time_signature(midi)
        estimated_key = self._estimate_key(midi)

        note_count = sum(len(instr.notes) for instr in midi.instruments)
        track_count = len(midi.instruments)

        note_density = self._calculate_note_density(midi, duration)

        return {
            "duration_seconds": round(duration, 2),
            "tempo_bpm": round(tempo, 2),
            "time_signature": time_signature,
            "estimated_key": estimated_key,
            "note_count": note_count,
            "track_count": track_count,
            "note_density": note_density,
            "chord_progression": []  # intentionally empty for v1
        }

    def _estimate_tempo(self, midi):
        tempos = midi.get_tempo_changes()[1]
        return float(np.mean(tempos)) if len(tempos) > 0 else 0.0

    def _extract_time_signature(self, midi):
        if midi.time_signature_changes:
            ts = midi.time_signature_changes[0]
            return f"{ts.numerator}/{ts.denominator}"
        return "unknown"

    def _estimate_key(self, midi):
        pitch_class_energy = np.zeros(12)

        for instrument in midi.instruments:
            for note in instrument.notes:
                pitch_class_energy[note.pitch % 12] += note.end - note.start

        key_index = int(np.argmax(pitch_class_energy))
        keys = ["C", "C#", "D", "D#", "E", "F",
                "F#", "G", "G#", "A", "A#", "B"]

        return keys[key_index]

    def _calculate_note_density(self, midi, duration):
        total_notes = sum(len(instr.notes) for instr in midi.instruments)

        avg_density = total_notes / duration if duration > 0 else 0

        return {
            "avg_notes_per_second": round(avg_density, 2),
            "peak_notes_per_second": round(avg_density * 1.5, 2)
        }