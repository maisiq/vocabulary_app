import pytest
from httpx import AsyncClient

from fastapi.testclient import TestClient

from src.words.routes.words import words
from src.main import app


client = TestClient(app)
