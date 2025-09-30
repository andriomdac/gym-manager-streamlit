from src.client.token import TokenAPIClient
import streamlit as st
from icecream import ic

def add_value_to_session(key: str, value: Any):
    pass

class Login:
    def __init__(self) -> None:
        pass

    def get_login_access(self, username: str, password: str):
        client = TokenAPIClient()
        response = client.get_token(username=username, password=password)
        if response.status_code == 200:
            st.session_state["access_token"] = response.json()["access"]
            st.rerun()
        elif response.status_code == 401:
            return response.json()["detail"]
        elif response.status_code == 400:
            return "Por favor, forneça um usuário e senha válidos."
        else:
            return response.json()

    def access_token_is_valid(self, access_token: str):
        client = TokenAPIClient()
        response = client.verify_token(access_token=access_token)
        if response.status_code == 200:
            return True
        return False

    def refresh_token(self, refresh_token: str):
        client = TokenAPIClient()
        response = client.refresh_token(refresh_token=refresh_token)
        if response.status_code == 200:
            new_access_tk = response.json()["access"]
            :w
