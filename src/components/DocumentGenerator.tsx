'use client';

import { useState } from 'react';
import { generateMockDocument } from '@/lib/mockDocumentGenerator';

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

  function handleGenerate() {
    setDraft(generateMockDocument(selectedTemplate, prompt));
  }

  function handleClear() {
    setPrompt('');
    setDraft('');
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
          placeholder="Ejemplo: crea una propuesta comercial para una escuela que necesita automatizar documentos administrativos."
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
            <button className="secondary-button" type="button">Exportar proximamente</button>
          </div>
          <pre className="draft-output">{draft}</pre>
        </section>
      ) : null}
    </div>
  );
}
