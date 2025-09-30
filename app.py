from re import sub
import streamlit as st
from src.service.login import Login


with st.container(key="login"):
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha")

    submit = st.button("Acessar")
    if submit:
        client = Login()
        st.info(client.get_login_access(username=username, password=password))


if "access_token" in st.session_state:
    client = Login()

    if not client.access_token_is_valid(access_token=st.session_state["access_token"]):
        pass
