import { useState } from "react";

import { listNotes } from "@/client";
import type { NoteResponse } from "@/client";

export function NoteList() {
  const [notes, setNotes] = useState<NoteResponse[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function loadNotes() {
    setLoading(true);
    setError(null);
    try {
      const { data } = await listNotes({ throwOnError: true });
      setNotes(data);
    } catch {
      setError("Could not load notes. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <button type="button" onClick={loadNotes} disabled={loading}>
        {loading ? "Loading..." : "Load notes"}
      </button>

      {error && <p role="alert">{error}</p>}
      {notes?.length === 0 && <p>No notes yet.</p>}
      {notes && notes.length > 0 && (
        <ul>
          {notes.map((note) => (
            <li key={note.id}>{note.body}</li>
          ))}
        </ul>
      )}
    </section>
  );
}
