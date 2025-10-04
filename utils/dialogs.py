import streamlit as st


@st.dialog("Erro ao executar ação:")
def error_dialog(message: str):
    st.error(f"{message}")

@st.dialog("Sucesso!")
def success_dialog(message: str):
    st.success(f"{message}")
