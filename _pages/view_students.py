from typing import Union
import streamlit as st
import streamlit_antd_components as sac
from src.client import StudentAPIClient
from icecream import ic


st.set_page_config(page_title="view_students")


def switch_to_view(
    to_view: Union[str, None] = None
    ) -> None:

    if to_view:
        st.session_state["view"] = to_view
    else:
        del st.session_state["view"]
    st.rerun()


def detail_student():
    with st.container():
        if st.button("<- Voltar à lista"):
            switch_to_view()

    with st.container():
        st.header("Detalhes do Aluno")


def list_students():
    st.header("Lista de Alunos")
    with st.container():
        search_input = st.text_input(label="Buscar", placeholder="Pesquisar por nome...")
        submit_button = st.button(label="Buscar", use_container_width=True, type="primary", )

    with st.container():
        students = StudentAPIClient().get_students().json()
        for student in students:    
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 3, 2])
                with col1:
                    st.write(student["name"])
                with col2:
                    st.write(student["reference"])
                with col3:
                    payment_btn = st.button(label="+Pagamento", key=f"payment-{student["id"]}", use_container_width=True)
                    detail_btn = st.button(label="Detalhes", key=f"detail-{student["id"]}", use_container_width=True)

                    if detail_btn:
                        st.session_state["selected_student_id"] = student["id"]
                        switch_to_view("detail")

def view_students():

    if "view" in st.session_state:
        view = st.session_state['view']
        if view == "detail":
            detail_student()

    else:
        list_students()
                                
                                