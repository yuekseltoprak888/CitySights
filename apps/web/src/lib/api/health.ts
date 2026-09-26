import { apiBaseUrl } from "@/lib/api/client";

export type ServiceHealth = {
  status: "ok" | "degraded";
  environment: string;
  country: string;
  database: "ok" | "unavailable";
  postgis: "ok" | "unavailable";
};

export type HealthView = ServiceHealth | { status: "unreachable" };

type LoadHealthOptions = {
  fetchImpl?: typeof fetch;
  baseUrl?: string;
};

export async function loadHealth(options: LoadHealthOptions = {}): Promise<HealthView> {
  const fetchImpl = options.fetchImpl ?? fetch;
  const baseUrl = options.baseUrl ?? apiBaseUrl();
  try {
    const response = await fetchImpl(`${baseUrl}/api/v1/health`, {
      cache: "no-store",
      headers: { accept: "application/json" },
    });
    if (response.status === 200 || response.status === 503) {
      return (await response.json()) as ServiceHealth;
    }
    return { status: "unreachable" };
  } catch {
    return { status: "unreachable" };
  }
}
