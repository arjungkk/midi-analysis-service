import pretty_midi

# Create a PrettyMIDI object with a fixed tempo
midi = pretty_midi.PrettyMIDI(initial_tempo=120)

# Create an instrument (Acoustic Grand Piano)
instrument = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program("Acoustic Grand Piano"))

# Define notes: C4, E4, G4, C5
notes = [
    ("C4", 0.0, 0.5),
    ("E4", 0.5, 1.0),
    ("G4", 1.0, 1.5),
    ("C5", 1.5, 2.0),
    ("G4", 2.0, 2.5),
    ("E4", 2.5, 3.0),
    ("C4", 3.0, 3.5),
]

for note_name, start, end in notes:
    note_number = pretty_midi.note_name_to_number(note_name)
    note = pretty_midi.Note(
        velocity=100,
        pitch=note_number,
        start=start,
        end=end
    )
    instrument.notes.append(note)

midi.instruments.append(instrument)

# Write MIDI file
output_path = "data/uploads/test_c_major_120bpm.mid"
midi.write(output_path)

print(f"Test MIDI written to {output_path}")
