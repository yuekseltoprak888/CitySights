import { describe, expect, it, vi } from "vitest";

import { ApiError, fetchJson } from "@/lib/api/client";
import { loadHealth } from "@/lib/api/health";
import { formatQuantity } from "@/lib/units";

describe("fetchJson", () => {
  it("returns a successful JSON body", async () => {
    const fetchImpl = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(JSON.stringify({ status: "ok" }), { status: 200 }),
    );

    await expect(fetchJson("/api/v1/health", undefined, fetchImpl)).resolves.toEqual({
      status: "ok",
    });
  });

  it("raises an API error with the server code", async () => {
    const fetchImpl = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(
        JSON.stringify({
          code: "organization_not_found",
          message: "Organization not found",
          details: {},
          request_id: "req-1",
        }),
        { status: 404, headers: { "content-type": "application/json" } },
      ),
    );

    await expect(fetchJson("/api/v1/organizations/missing", undefined, fetchImpl)).rejects.toMatchObject(
      {
        name: "ApiError",
        status: 404,
        code: "organization_not_found",
        requestId: "req-1",
      } satisfies Partial<ApiError>,
    );
  });

  it("converts a network failure into an API error", async () => {
    const fetchImpl = vi.fn<typeof fetch>().mockRejectedValue(new Error("offline"));
    await expect(fetchJson("/api/v1/health", undefined, fetchImpl)).rejects.toMatchObject({
      code: "network_error",
      status: 0,
    });
  });
});

describe("loadHealth", () => {
  it("keeps a degraded report when the API returns 503", async () => {
    const fetchImpl = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(
        JSON.stringify({
          status: "degraded",
          environment: "local",
          country: "CH",
          database: "unavailable",
          postgis: "unavailable",
        }),
        { status: 503 },
      ),
    );

    await expect(loadHealth({ fetchImpl, baseUrl: "http://api.test" })).resolves.toMatchObject({
      status: "degraded",
      database: "unavailable",
    });
  });
});

describe("formatQuantity", () => {
  it("formats Swiss numbers with a unit", () => {
    const formatted = new Intl.NumberFormat("de-CH", { maximumFractionDigits: 2 }).format(1200);
    expect(formatQuantity("1200", "kWh")).toBe(`${formatted} kWh`);
    expect(formatQuantity("42", "m2")).toBe(
      `${new Intl.NumberFormat("de-CH", { maximumFractionDigits: 2 }).format(42)} m²`,
    );
  });
});
