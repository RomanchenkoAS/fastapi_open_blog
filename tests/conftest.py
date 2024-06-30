import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database_definition import Base, get_db
from main import app


@pytest.fixture(scope="function")
def test_db():
    """
    Set up a test database for the duration of the testing session.
    Create the tables at the start and drop them at the end.
    """
    SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    yield TestingSessionLocal()

    Base.metadata.drop_all(bind=engine)
    os.remove("test.db")


@pytest.fixture(scope="function")
def test_client(test_db):
    """
    Set up a TestClient for the FastAPI app and override the get_db dependency.
    """

    def override_get_db() -> Generator:
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
