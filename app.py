import streamlit as st


with st.container(key="login"):
    username = st.text_input("Usuário")
    password = st.text_input("Senha")

    submit = st.button("Acessar")
