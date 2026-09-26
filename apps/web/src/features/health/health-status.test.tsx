import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { HealthStatus } from "@/features/health/health-status";

describe("HealthStatus", () => {
  it("shows a reachable platform report", () => {
    render(
      <HealthStatus
        health={{
          status: "ok",
          environment: "local",
          country: "CH",
          database: "ok",
          postgis: "ok",
        }}
      />,
    );

    expect(screen.getByRole("status").textContent).toContain("Platform status");
    expect(screen.getByRole("status").textContent).toContain("CH");
    expect(screen.getByRole("status").textContent).toContain("PostGIS");
  });

  it("shows an unreachable API", () => {
    render(<HealthStatus health={{ status: "unreachable" }} />);
    expect(screen.getByRole("status").textContent).toContain("API unreachable");
  });
});
