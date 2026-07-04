import { AppShell } from '@/components/AppShell';

const stats = [
  { label: 'Documentos', value: '0' },
  { label: 'Creditos IA', value: '100' },
  { label: 'Plantillas', value: '6' }
];

export default function DashboardPage() {
  return (
    <AppShell>
      <div className="page-header">
        <div>
          <p className="eyebrow">MVP</p>
          <h2>Dashboard</h2>
          <p className="muted">Centro de trabajo para crear documentos con IA.</p>
        </div>
        <a className="primary-button" href="/new-document">Nuevo documento</a>
      </div>

      <div className="stats-grid">
        {stats.map((stat) => (
          <div className="card" key={stat.label}>
            <p className="muted">{stat.label}</p>
            <strong className="stat-value">{stat.value}</strong>
          </div>
        ))}
      </div>

      <div className="card mt-6">
        <h3>Primer objetivo</h3>
        <p className="muted">Crear el primer documento generado por IA y exportarlo.</p>
      </div>
    </AppShell>
  );
}
