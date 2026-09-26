"""Physical energy calculations.

Engines in this package return Result values with units and assumptions.
They do not import finance, FastAPI, SQLAlchemy, or provider clients.
"""

from energyos.domain.ports import EnergyEngine

__all__ = ["EnergyEngine"]
