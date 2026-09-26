# Swiss data providers

Switzerland is the only supported country. Each external dataset is a port plus an adapter. Tests keep the mock adapter, which returns no surveyed coordinates, yields, tariff rates, or subsidy amounts.

| Need | Likely source | Port |
| --- | --- | --- |
| Address search and coordinates | geo.admin / swisstopo | `AddressProvider` |
| Building footprint and attributes | GWR via geo.admin | `BuildingDataProvider` |
| Roof solar potential | BFE Sonnendach | `SolarPotentialProvider` |
| Irradiance or weather | MeteoSwiss, with PVGIS only when marked as a non-official source | `WeatherProvider` |
| Electricity tariff | Utility and ElCom data, keyed by municipality, utility, and year | `TariffProvider` |
| Subsidies | Pronovo and canton programs, with effective dates | `SubsidyProvider` |

An adapter maps external fields into domain quantities and records the source name and retrieval date on the assumption set. Confirm the license and the access terms before implementing an adapter.

The browser calls EnergyOS only. Provider URLs stay in the adapter.

Tariff data is a schedule with periods, not a single price. Subsidy programs carry effective dates. If a provider is not configured, the adapter returns an empty result and an assumption that says the source is unavailable.
