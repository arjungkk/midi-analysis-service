import { useState } from "react";

export default function MidiClient() {
  const [file, setFile] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [params, setParams] = useState({ semitones: 2, tempoFactor: 1.2 });

  const uploadMidi = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/midi", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setJobId(data.midi_id);
  };

  const runTranspose = async () => {
    const res = await fetch(`http://localhost:8000/midi/${jobId}/transpose?semitones=${params.semitones}`, {
      method: "POST",
    });
    const data = await res.json();
    setStatus(data);
  };

  const runTempo = async () => {
    const res = await fetch(`http://localhost:8000/midi/${jobId}/tempo?factor=${params.tempoFactor}`, {
      method: "POST",
    });
    const data = await res.json();
    setStatus(data);
  };

  return (
    <div className="p-6 max-w-xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">MIDI Transformation Demo</h1>

      <input type="file" accept=".mid" onChange={(e) => setFile(e.target.files[0])} />
      <button className="btn" onClick={uploadMidi} disabled={!file}>Upload MIDI</button>

      {jobId && (
        <div className="space-y-2">
          <div>Job ID: {jobId}</div>

          <div className="flex gap-2">
            <input
              type="number"
              value={params.semitones}
              onChange={(e) => setParams({ ...params, semitones: e.target.value })}
            />
            <button className="btn" onClick={runTranspose}>Transpose</button>
          </div>

          <div className="flex gap-2">
            <input
              type="number"
              step="0.1"
              value={params.tempoFactor}
              onChange={(e) => setParams({ ...params, tempoFactor: e.target.value })}
            />
            <button className="btn" onClick={runTempo}>Change Tempo</button>
          </div>
        </div>
      )}

      {status && (
        <pre className="bg-gray-100 p-2 text-sm">{JSON.stringify(status, null, 2)}</pre>
      )}
    </div>
  );
}
