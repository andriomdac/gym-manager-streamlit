import streamlit as st
import streamlit_antd_components as sac
from src.client import StudentAPIClient
from icecream import ic 
from _pages.login import login_verifier

st.set_page_config(page_title="add_student")
client = StudentAPIClient()


@login_verifier
def add_student():
    with st.container():
        st.header("Matricular Aluno")

        with st.container():
            with st.form(key="add_student"):    
                name = st.text_input("Nome")
                phone = st.text_input("Telefone")
                reference = st.text_area("Referência")

                submit = st.form_submit_button("Matricular", use_container_width=True)

                if submit:
                    data = {}
                    data['name'] = name
                    data['phone'] = phone
                    data['reference'] = reference

                    response = client.add_student(data=data)
                    if response.status_code == 201:
                        st.success("Aluno Adicionado")
                    else:
                        st.error(f"{response.json()}")
                    


            