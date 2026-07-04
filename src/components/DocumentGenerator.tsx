'use client';

import { useState } from 'react';
import { generateMockDocument } from '@/lib/mockDocumentGenerator';
import { saveDocument } from '@/lib/documentService';

const templates = [
  'Carta formal',
  'Propuesta comercial',
  'Plan de clase',
  'Contrato simple',
  'Descripcion de producto',
  'Correo profesional'
];

export function DocumentGenerator() {
  const [selectedTemplate, setSelectedTemplate] = useState(templates[0]);
  const [prompt, setPrompt] = useState('');
  const [draft, setDraft] = useState('');
  const [saveMessage, setSaveMessage] = useState('');

  function handleGenerate() {
    setDraft(generateMockDocument(selectedTemplate, prompt));
    setSaveMessage('');
  }

  function handleClear() {
    setPrompt('');
    setDraft('');
    setSaveMessage('');
  }

  async function handleSave() {
    if (!draft) return;
    setSaveMessage('Guardando...');
    const title = prompt.trim().slice(0, 60) || selectedTemplate;
    const result = await saveDocument({ title, template: selectedTemplate, content: draft });
    setSaveMessage(result.error ? result.error : 'Documento guardado.');
  }

  return (
    <div className="two-column">
      <section className="card">
        <h3>Plantillas</h3>
        <div className="template-list">
          {templates.map((template) => (
            <button
              className={template === selectedTemplate ? 'template-button selected' : 'template-button'}
              key={template}
              onClick={() => setSelectedTemplate(template)}
              type="button"
            >
              {template}
            </button>
          ))}
        </div>
      </section>

      <section className="card">
        <h3>Instrucciones</h3>
        <p className="muted">Plantilla seleccionada: {selectedTemplate}</p>
        <label className="field-label" htmlFor="prompt">Describe el documento</label>
        <textarea
          id="prompt"
          className="textarea"
          value={prompt}
          onChange={(event) => setPrompt(event.target.value)}
          placeholder="Ejemplo: crea una propuesta comercial para una escuela."
        />
        <div className="button-row">
          <button className="primary-button" onClick={handleGenerate} type="button">Generar borrador</button>
          <button className="secondary-button" onClick={handleClear} type="button">Limpiar</button>
        </div>
      </section>

      {draft ? (
        <section className="card document-preview">
          <div className="page-header compact">
            <div>
              <p className="eyebrow">Borrador</p>
              <h3>Documento generado</h3>
            </div>
            <button className="secondary-button" onClick={handleSave} type="button">Guardar</button>
          </div>
          {saveMessage ? <p className="muted">{saveMessage}</p> : null}
          <pre className="draft-output">{draft}</pre>
        </section>
      ) : null}
    </div>
  );
}
