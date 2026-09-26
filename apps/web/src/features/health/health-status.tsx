import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { HealthView } from "@/lib/api/health";

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="grid grid-cols-[8rem_1fr] gap-4 border-t border-border py-3 first:border-t-0">
      <dt className="text-muted-foreground">{label}</dt>
      <dd>{value}</dd>
    </div>
  );
}

export function HealthStatus({ health }: { health: HealthView }) {
  if (health.status === "unreachable") {
    return (
      <Card role="status">
        <CardHeader>
          <CardTitle>API unreachable</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">The EnergyOS API did not respond.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card role="status">
      <CardHeader>
        <CardTitle>Platform status</CardTitle>
      </CardHeader>
      <CardContent>
        <dl>
          <Row label="Service" value={health.status} />
          <Row label="Database" value={health.database} />
          <Row label="PostGIS" value={health.postgis} />
          <Row label="Environment" value={health.environment} />
          <Row label="Country" value={health.country} />
        </dl>
      </CardContent>
    </Card>
  );
}
