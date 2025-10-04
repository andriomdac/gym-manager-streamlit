import streamlit as st
from src.service.session import Session
import streamlit_antd_components as sac


Session().validate_session()

if "access_token" in st.session_state:
    with st.container():
        with st.sidebar:
            st.subheader("Navegação")
            menu = sac.menu(
                items=[
                    sac.MenuItem(
                        label="Painel",
                        icon="bi bi-house-door-fill"
                    ),
                ],
                color="blue"
            )

else:
    with st.container():
        st.title("Acessar")

        with st.form(key="login-form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")

            submit = st.form_submit_button(label="Entrar")
            if submit:
                Session().get_login_access(username=username, password=password)
