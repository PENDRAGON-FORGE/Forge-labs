import Link from 'next/link';

const navItems = [
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/new-document', label: 'Nuevo documento' },
  { href: '/history', label: 'Historial' },
  { href: '/settings', label: 'Configuracion' },
  { href: '/login', label: 'Login' }
];

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <aside className="sidebar">
        <div>
          <p className="brand-kicker">Forge Labs</p>
          <h1 className="brand-title">Workspace</h1>
        </div>
        <nav className="nav-list">
          {navItems.map((item) => (
            <Link key={item.href} className="nav-link" href={item.href}>
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <section className="app-content">{children}</section>
    </main>
  );
}
