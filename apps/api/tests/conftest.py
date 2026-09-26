import os

os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://energyos:energyos@localhost:5432/energyos",
)
os.environ.setdefault("CORS_ORIGINS", "http://localhost:3000")
