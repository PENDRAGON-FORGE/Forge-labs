import { AppShell } from '@/components/AppShell';

const plans = [
  { name: 'Free', price: '$0 MXN', description: 'Prueba inicial con creditos limitados.' },
  { name: 'Pro', price: '$199 MXN/mes', description: 'Mas documentos, exportacion y plantillas premium.' },
  { name: 'Business', price: '$499 MXN/mes', description: 'Equipos, historial avanzado y uso empresarial.' }
];

export default function SubscriptionPage() {
  return (
    <AppShell>
      <div className="page-header">
        <div>
          <p className="eyebrow">Monetizacion</p>
          <h2>Suscripcion</h2>
          <p className="muted">Primer modelo de precios para validar ingresos.</p>
        </div>
      </div>
      <div className="stats-grid">
        {plans.map((plan) => (
          <section className="card" key={plan.name}>
            <h3>{plan.name}</h3>
            <strong className="stat-value">{plan.price}</strong>
            <p className="muted">{plan.description}</p>
          </section>
        ))}
      </div>
    </AppShell>
  );
}
