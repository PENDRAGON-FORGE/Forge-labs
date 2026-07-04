export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="mx-auto flex min-h-screen max-w-5xl flex-col justify-center px-6">
        <p className="mb-4 text-sm font-semibold uppercase tracking-[0.3em] text-cyan-300">
          Forge Labs
        </p>
        <h1 className="max-w-3xl text-5xl font-bold leading-tight">
          Menos trabajo repetitivo. Mas tiempo para crear.
        </h1>
        <p className="mt-6 max-w-2xl text-lg text-slate-300">
          Primer MVP: Forge Workspace con Documents AI. Genera, edita,
          guarda y exporta documentos asistidos por IA.
        </p>
        <div className="mt-10 flex gap-4">
          <a className="rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950" href="/dashboard">
            Abrir dashboard
          </a>
          <a className="rounded-xl border border-slate-700 px-5 py-3 font-semibold text-slate-100" href="/new-document">
            Crear documento
          </a>
        </div>
      </section>
    </main>
  );
}
