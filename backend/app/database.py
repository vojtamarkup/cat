import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Adresa databáze. Výchozí hodnota sedí na Postgres z compose.yaml.
# Později ji v Dockeru/Kubernetes přepíšeme proměnnou prostředí.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://cat:cat@localhost:5433/cat")

# Engine = připojení k databázi
engine = create_engine(DATABASE_URL)

# Továrna na "sezení" (session) = jedna práce s databází
SessionLocal = sessionmaker(bind=engine)


# Základ pro všechny tabulky
class Base(DeclarativeBase):
    pass


# Pro každý požadavek otevře session a po něm ji zavře
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
