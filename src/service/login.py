from client import token


class Login:
    def __init__(self) -> None:
        pass

    def get_login_access(username: str, password: str):
        client = token.TokenAPIClient()
        response = client.get_token(username=username, password=password)
