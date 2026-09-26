import { HealthStatus } from "@/features/health/health-status";
import { loadHealth } from "@/lib/api/health";

export default async function HomePage() {
  const health = await loadHealth();

  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col justify-between px-6 py-10">
      <header className="flex items-center justify-between text-sm tracking-wide text-muted-foreground">
        <span>EnergyOS</span>
        <span>Switzerland</span>
      </header>
      <section className="space-y-8">
        <div className="space-y-4">
          <p className="text-sm uppercase tracking-[0.18em] text-muted-foreground">
            Assessment platform
          </p>
          <h1 className="font-serif text-6xl leading-none">EnergyOS</h1>
          <p className="max-w-xl text-lg text-muted-foreground">
            B2B energy assessment for commercial and residential properties in Switzerland.
          </p>
        </div>
        <HealthStatus health={health} />
      </section>
      <footer className="text-sm text-muted-foreground">
        Foundation shell. The assessment workflow is not available yet.
      </footer>
    </main>
  );
}
