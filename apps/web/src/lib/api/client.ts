export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly requestId: string | null;

  constructor(status: number, code: string, message: string, requestId: string | null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.requestId = requestId;
  }
}

export function apiBaseUrl(): string {
  if (typeof window === "undefined") {
    return process.env.API_BASE_URL ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
  }
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
}

function errorFields(body: unknown): { code: string; message: string; requestId: string | null } {
  if (typeof body !== "object" || body === null) {
    return { code: "http_error", message: "Request failed", requestId: null };
  }
  const record = body as Record<string, unknown>;
  return {
    code: typeof record.code === "string" ? record.code : "http_error",
    message: typeof record.message === "string" ? record.message : "Request failed",
    requestId: typeof record.request_id === "string" ? record.request_id : null,
  };
}

export async function fetchJson<T>(
  path: string,
  init?: RequestInit,
  fetchImpl: typeof fetch = fetch,
): Promise<T> {
  let response: Response;
  try {
    response = await fetchImpl(`${apiBaseUrl()}${path}`, {
      ...init,
      headers: {
        accept: "application/json",
        ...init?.headers,
      },
      cache: "no-store",
    });
  } catch {
    throw new ApiError(0, "network_error", "The EnergyOS API did not respond", null);
  }

  if (!response.ok) {
    const body: unknown = await response.json().catch(() => null);
    const fields = errorFields(body);
    throw new ApiError(response.status, fields.code, fields.message, fields.requestId);
  }

  return (await response.json()) as T;
}
