import { AppShell } from '@/components/AppShell';

const templates = [
  'Carta formal',
  'Propuesta comercial',
  'Plan de clase',
  'Contrato simple',
  'Descripcion de producto',
  'Correo profesional'
];

export default function NewDocumentPage() {
  return (
    <AppShell>
      <div className="page-header">
        <div>
          <p className="eyebrow">Documents AI</p>
          <h2>Nuevo documento</h2>
          <p className="muted">Selecciona una plantilla y describe lo que necesitas.</p>
        </div>
      </div>

      <div className="two-column">
        <section className="card">
          <h3>Plantillas</h3>
          <div className="template-list">
            {templates.map((template) => (
              <button className="template-button" key={template}>{template}</button>
            ))}
          </div>
        </section>

        <section className="card">
          <h3>Instrucciones</h3>
          <label className="field-label" htmlFor="prompt">Describe el documento</label>
          <textarea id="prompt" className="textarea" placeholder="Ejemplo: crea una propuesta comercial para una escuela que necesita automatizar documentos administrativos." />
          <button className="primary-button full-width">Generar borrador</button>
        </section>
      </div>
    </AppShell>
  );
}
