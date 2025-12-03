import pytest
import tempfile
import os
from db import init_db, DB_NAME


@pytest.fixture
def temp_db(monkeypatch):
    """Создаёт временную БД для тестов"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_file.close()

    monkeypatch.setattr("db.DB_NAME", temp_file.name)

    init_db()

    yield temp_file.name

    try:
        os.unlink(temp_file.name)
    except (PermissionError, FileNotFoundError):
        pass
