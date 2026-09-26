const unitLabels: Record<string, string> = {
  kWh: "kWh",
  kW: "kW",
  kWp: "kWp",
  m2: "m²",
  CHF: "CHF",
  "CHF/kWh": "CHF/kWh",
  percent: "%",
  "1": "",
};

export function formatQuantity(value: string, unit: string): string {
  const amount = Number(value);
  if (!Number.isFinite(amount)) {
    return unit ? `${value} ${unitLabels[unit] ?? unit}`.trim() : value;
  }
  const formatted = new Intl.NumberFormat("de-CH", {
    maximumFractionDigits: 2,
  }).format(amount);
  const label = unitLabels[unit] ?? unit;
  return label ? `${formatted} ${label}` : formatted;
}
