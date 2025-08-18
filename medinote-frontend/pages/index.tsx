import { useState, FormEvent } from 'react';

export default function Home() {
  const [vitals, setVitals] = useState('');
  const [labs, setLabs] = useState('');
  const [meds, setMeds] = useState('');
  const [symptoms, setSymptoms] = useState('');
  const [note, setNote] = useState('');

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const payload = {
      vitals: { notes: vitals },
      labs: { notes: labs },
      active_meds: meds.split(',').map(m => m.trim()).filter(Boolean),
      problems: symptoms.split(',').map(s => s.trim()).filter(Boolean)
    };

    try {
      const res = await fetch('http://localhost:8000/generate-note', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      setNote(JSON.stringify(data, null, 2));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <main style={{ padding: '2rem' }}>
      <h1>MediNote</h1>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: '600px' }}>
        <label>
          Vitals
          <textarea value={vitals} onChange={e => setVitals(e.target.value)} />
        </label>
        <label>
          Labs
          <textarea value={labs} onChange={e => setLabs(e.target.value)} />
        </label>
        <label>
          Meds (comma separated)
          <textarea value={meds} onChange={e => setMeds(e.target.value)} />
        </label>
        <label>
          Symptoms (comma separated)
          <textarea value={symptoms} onChange={e => setSymptoms(e.target.value)} />
        </label>
        <button type="submit">Generate Note</button>
      </form>
      {note && (
        <pre style={{ marginTop: '2rem', whiteSpace: 'pre-wrap' }}>{note}</pre>
      )}
    </main>
  );
}
