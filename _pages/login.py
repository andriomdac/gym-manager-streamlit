import streamlit as st
import streamlit_antd_components as sac
from src.client import TokenAPIClient
from icecream import ic


def login_verifier(func):
    def wrapper(*args, **kwargs):
        if "token" in st.session_state:
            return func()
        else:
            return login()
    return wrapper


def add_token_to_session(token:str):
    st.session_state['token'] = token


def login():
    st.title("🔐 Acessar")
    st.markdown("---")
    
    with st.form("login_form"):
        st.subheader("Insira suas credenciais")
        
        username = st.text_input(
            "Usuário",
            placeholder="Digite seu usuário",
            help="Seu usuário de cadastro"
        )
        
        password = st.text_input(
            "Senha",
            type="password",
            placeholder="Digite sua senha",
            help="Sua senha de acesso"
        )
        

        submitted = st.form_submit_button(
            "Acessar",
            type="primary",
            use_container_width=True
        )
        
        if submitted:

            if not username:
                st.error("Por favor, insira seu usuário")
            elif not password:
                st.error("Por favor, insira a sua senha")
            else:
                token_client = TokenAPIClient()
                response = token_client.get_token(username=username, password=password)
                
                if response.status_code == 200:
                    token = response.json()["access"]
                    add_token_to_session(token=token)
                    st.rerun()
                else:
                    st.error("Falhar ao acessar. Verifique usuário e/ou senha")
                    