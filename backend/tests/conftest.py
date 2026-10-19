import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

# Testovací databáze (port uprav podle compose.yaml: 5432 nebo 5433)
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql+psycopg://cat:cat@localhost:5433/cat_test")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


# Fixture = příprava, kterou si test vyžádá parametrem "client"
@pytest.fixture
def client():
    # Před testem: vytvoř čisté tabulky
    Base.metadata.create_all(bind=engine)

    # Místo skutečné databáze dej aplikaci testovací
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # TestClient posílá požadavky přímo do aplikace (bez uvicornu) DÍKY TOMU NEMUSÍ BĚŽET SERVER
    with TestClient(app) as test_client:
        yield test_client

    # Po testu: ukliď
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
