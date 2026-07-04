'use client';

import { useEffect, useState } from 'react';
import { getDocumentById, updateDocument } from '@/lib/documentService';

type Props = { id: string };

export function DocumentEditor({ id }: Props) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [message, setMessage] = useState('Cargando documento...');

  useEffect(() => {
    async function loadDocument() {
      const result = await getDocumentById(id);
      if (result.error || !result.data) {
        setMessage(result.error || 'Documento no encontrado');
        return;
      }
      setTitle(result.data.title || 'Documento');
      setContent(result.data.content || '');
      setMessage('');
    }

    loadDocument();
  }, [id]);

  async function handleSave() {
    setMessage('Guardando cambios...');
    const result = await updateDocument({ id, title, content });
    setMessage(result.error ? result.error : 'Cambios guardados.');
  }

  async function handleCopy() {
    await navigator.clipboard.writeText(content);
    setMessage('Contenido copiado.');
  }

  return (
    <div className="card editor-card">
      <label className="field-label" htmlFor="title">Titulo</label>
      <input id="title" className="input" value={title} onChange={(event) => setTitle(event.target.value)} />

      <label className="field-label" htmlFor="content">Contenido</label>
      <textarea id="content" className="textarea editor-textarea" value={content} onChange={(event) => setContent(event.target.value)} />

      <div className="button-row">
        <button className="primary-button" onClick={handleSave} type="button">Guardar cambios</button>
        <button className="secondary-button" onClick={handleCopy} type="button">Copiar contenido</button>
      </div>

      {message ? <p className="muted">{message}</p> : null}
    </div>
  );
}
