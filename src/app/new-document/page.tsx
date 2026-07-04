import { AppShell } from '@/components/AppShell';
import { DocumentGenerator } from '@/components/DocumentGenerator';

export default function NewDocumentPage() {
  return (
    <AppShell>
      <div className="page-header">
        <div>
          <p className="eyebrow">Documents AI</p>
          <h2>Nuevo documento</h2>
          <p className="muted">Selecciona una plantilla y genera un borrador.</p>
        </div>
      </div>
      <DocumentGenerator />
    </AppShell>
  );
}
