import pytest
from utils.api_client import APIClient
from config import REQRES_API_KEY

REQRES_BASE_URL = "https://reqres.in/api"


@pytest.fixture(scope="session")
def reqres_api():
    """API client pointed at reqres.in, authenticated with x-api-key header."""
    client = APIClient(base_url=REQRES_BASE_URL, token="")
    if REQRES_API_KEY:
        client.session.headers["x-api-key"] = REQRES_API_KEY
    return client
