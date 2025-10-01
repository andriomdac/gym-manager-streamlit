from re import sub
import streamlit as st
from src.service.session import Session
from icecream import ic


Session().validate_session()
if "access_token" in st.session_state:
    with st.sidebar:
        st.title("Navegação")
else:
    with st.container():
        st.title("Acessar")

        with st.form(key="login-form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")

            submit = st.form_submit_button(label="Entrar")
            if submit:
                Session().get_login_access(username=username, password=password)
