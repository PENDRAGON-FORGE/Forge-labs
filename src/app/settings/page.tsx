import { AppShell } from '@/components/AppShell';

export default function SettingsPage() {
  return (
    <AppShell>
      <div className="page-header">
        <div>
          <p className="eyebrow">Cuenta</p>
          <h2>Configuracion</h2>
          <p className="muted">Configuracion inicial del workspace.</p>
        </div>
      </div>
      <div className="two-column">
        <section className="card">
          <h3>Perfil</h3>
          <p className="muted">Nombre, correo y preferencias del usuario.</p>
        </section>
        <section className="card">
          <h3>Plan</h3>
          <p className="muted">Plan gratuito inicial con creditos de prueba.</p>
          <a className="primary-button" href="/subscription">Ver suscripcion</a>
        </section>
      </div>
    </AppShell>
  );
}
