import { AppShell } from '@/components/AppShell';
import { mockDocuments } from '@/lib/mockDocuments';

export default function HistoryPage() {
  return (
    <AppShell>
      <div className="page-header">
        <div>
          <p className="eyebrow">Archivo</p>
          <h2>Historial</h2>
          <p className="muted">Documentos recientes del workspace.</p>
        </div>
        <a className="primary-button" href="/new-document">Crear documento</a>
      </div>

      <div className="history-list">
        {mockDocuments.map((document) => (
          <article className="card history-item" key={document.id}>
            <div>
              <p className="eyebrow">{document.template}</p>
              <h3>{document.title}</h3>
              <p className="muted">Creado: {document.createdAt}</p>
            </div>
            <span className="status-pill">{document.status}</span>
          </article>
        ))}
      </div>
    </AppShell>
  );
}
