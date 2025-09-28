import requests as rq

BASE_URL = "http://localhost:8000/api"


class TokenAPIClient:
    def __init__(self) -> None:
        self._base_url = f"{BASE_URL}/token/"

    def get_token(self, username: str, password: str):
        return rq.api.post(
            url=f"{self._base_url}", json={"username": username, "password": password}
        )
