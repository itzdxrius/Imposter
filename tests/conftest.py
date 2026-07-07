import os
import sys

os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("GOOGLE_CLIENT_ID", "test-client-id")
os.environ.setdefault("GOOGLE_CLIENT_SECRET", "test-client-secret")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from app import create_app


@pytest.fixture
def app():
    application = create_app()
    application.config.update(TESTING=True)
    with application.app_context():
        yield application


@pytest.fixture
def client(app):
    return app.test_client()