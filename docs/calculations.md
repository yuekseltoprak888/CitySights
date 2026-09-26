# Calculations

No energy or financial calculation is implemented in the foundation.

When they are added:

- Physical calculations live in `domain/energy` and return `Result`.
- Financial calculations live in `domain/finance`. They receive energy results and a `TariffSchedule`. They do not call pvlib, a weather API, or a tariff API.
- Every result includes the assumptions that affected it and the engine version.
- Assumptions name their unit, source, and effective date.
- NumPy, pandas, pvlib, and SciPy belong in the optional `energy` dependency group of `apps/api`.
- Pyomo stays out until an optimization problem exists.
- Do not hardcode electricity prices, subsidies, degradation, performance ratio, self-consumption, or discount rates. Those values enter as data or as an assumption set.
