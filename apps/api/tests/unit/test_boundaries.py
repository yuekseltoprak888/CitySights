import ast
from pathlib import Path

API_ROOT = Path(__file__).resolve().parents[2]
SOURCE = API_ROOT / "src" / "energyos"

INFRASTRUCTURE = {
    "fastapi",
    "sqlalchemy",
    "httpx",
    "requests",
    "pvlib",
    "pandas",
    "numpy",
    "scipy",
    "pyomo",
    "energyos.integrations",
    "energyos.db",
    "energyos.api",
    "energyos.services",
    "energyos.main",
    "energyos.composition",
}


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def assert_clean(root: Path, forbidden: set[str]) -> None:
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        for module in imported_modules(path):
            for prefix in forbidden:
                if module == prefix or module.startswith(prefix + "."):
                    offenders.append(f"{path.relative_to(API_ROOT)} imports {module}")
    assert offenders == []


def test_domain_and_services_stay_free_of_infrastructure() -> None:
    assert_clean(SOURCE / "domain", INFRASTRUCTURE)
    assert_clean(
        SOURCE / "services",
        INFRASTRUCTURE - {"energyos.services"}
        | {"energyos.main", "energyos.composition", "energyos.api", "energyos.db"},
    )


def test_energy_and_finance_do_not_import_each_other() -> None:
    assert_clean(SOURCE / "domain" / "energy", {"energyos.domain.finance"})
    assert_clean(SOURCE / "domain" / "finance", {"energyos.domain.energy"})


def test_routes_do_not_import_persistence_or_providers() -> None:
    route_files = [
        SOURCE / "api" / "health.py",
        SOURCE / "api" / "organizations.py",
        SOURCE / "api" / "assessments.py",
        SOURCE / "api" / "schemas.py",
        SOURCE / "api" / "router.py",
    ]
    forbidden = {"sqlalchemy", "energyos.db", "energyos.integrations"}
    offenders: list[str] = []
    for path in route_files:
        for module in imported_modules(path):
            for prefix in forbidden:
                if module == prefix or module.startswith(prefix + "."):
                    offenders.append(f"{path.name} imports {module}")
    assert offenders == []
