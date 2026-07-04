'use client';

import { useEffect, useState } from 'react';
import { listDocuments } from '@/lib/documentService';

type DocumentRow = {
  id: string;
  title: string;
  template: string | null;
  status: string | null;
  created_at: string;
};

export function DocumentHistory() {
  const [documents, setDocuments] = useState<DocumentRow[]>([]);
  const [message, setMessage] = useState('Cargando documentos...');

  useEffect(() => {
    async function loadDocuments() {
      const result = await listDocuments();
      if (result.error) {
        setMessage(result.error);
        return;
      }
      setDocuments(result.data as DocumentRow[]);
      setMessage('');
    }

    loadDocuments();
  }, []);

  if (message) {
    return <div className="card"><p className="muted">{message}</p></div>;
  }

  if (!documents.length) {
    return (
      <div className="card empty-state">
        <h3>Aun no hay documentos</h3>
        <p className="muted">Genera tu primer documento para verlo aqui.</p>
      </div>
    );
  }

  return (
    <div className="history-list">
      {documents.map((document) => (
        <article className="card history-item" key={document.id}>
          <div>
            <p className="eyebrow">{document.template || 'Documento'}</p>
            <h3>{document.title}</h3>
            <p className="muted">Creado: {new Date(document.created_at).toLocaleDateString()}</p>
          </div>
          <span className="status-pill">{document.status || 'draft'}</span>
        </article>
      ))}
    </div>
  );
}
