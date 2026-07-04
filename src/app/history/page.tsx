import { AppShell } from '@/components/AppShell';

export default function HistoryPage() {
  return (
    <AppShell>
      <div className="page-header">
        <div>
          <p className="eyebrow">Archivo</p>
          <h2>Historial</h2>
          <p className="muted">Aqui apareceran los documentos generados y sus versiones.</p>
        </div>
      </div>
      <div className="card empty-state">
        <h3>Aun no hay documentos</h3>
        <p className="muted">Genera tu primer documento para verlo en el historial.</p>
        <a className="primary-button" href="/new-document">Crear documento</a>
      </div>
    </AppShell>
  );
}
