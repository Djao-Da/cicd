import requests


class APIClient:
    def __init__(self, base_url: str, token: str = ""):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers["Content-Type"] = "application/json"
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def set_token(self, token: str):
        """Set or update the Bearer token for all subsequent requests."""
        self.session.headers["Authorization"] = f"Bearer {token}"

    def get(self, path, **kwargs):
        return self.session.get(f"{self.base_url}{path}", **kwargs)

    def post(self, path, **kwargs):
        return self.session.post(f"{self.base_url}{path}", **kwargs)

    def put(self, path, **kwargs):
        return self.session.put(f"{self.base_url}{path}", **kwargs)

    def patch(self, path, **kwargs):
        return self.session.patch(f"{self.base_url}{path}", **kwargs)

    def delete(self, path, **kwargs):
        return self.session.delete(f"{self.base_url}{path}", **kwargs)
