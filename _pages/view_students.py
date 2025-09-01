from typing import Union
import streamlit as st
import streamlit_antd_components as sac
from src.client import StudentAPIClient, PaymentAPIClient
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


def student_detail_card(student: dict):
    col1, col2, col3 = st.columns([3, 3, 2])
    with col1:
        st.write(student["name"])
    with col2:
        st.write(student["reference"])
    with col3:
        st.write(student["phone"])


def switch_to_view_button(message: str, to_view: Union[str, None] = None):
    with st.container():
        if st.button(message, use_container_width=True):
            switch_to_view(to_view)

def add_payment():
    student = st.session_state['selected_student']

    with st.container():
        student_detail_header(
            header="Adicionar Pagamento",
            return_to_btn_msg="<- Voltar aos detalhes",
            return_to_view="detail"
            )

    with st.container(border=True):
        student_detail_card(student=student)

    with st.container():
        with st.form(key="add_payment", enter_to_submit=True):
            payment_package = st.text_input("Pacote de Pagamento")
            observations = st.text_input("Observações")

            submit = st.form_submit_button(label="Próximo", use_container_width=True)
            if submit:
                data = {}
                data['payment_package'] = payment_package
                data['observations'] = observations
                new_payment = PaymentAPIClient(student_id=student["id"]).add_payment(data=data)
                st.info(new_payment.json())


def student_detail_header(header: str, return_to_btn_msg: str, return_to_view: str):
    with st.container():
        col1, col2 = st.columns([2, 1], vertical_alignment="bottom")
        with col1:
            st.header(header)
        with col2:
            switch_to_view_button(message=return_to_btn_msg, to_view=return_to_view)


def detail_student():
    student = st.session_state['selected_student']

    with st.container():
        student_detail_header(
            header="Detalhes do Aluno",
            return_to_btn_msg="<- Voltar à Lista de Alunos",
            return_to_view=None
            )

    with st.container(border=True):
        student_detail_card(student=student)

    with st.container():
        if st.button(label="Adicionar Pagamento"):
            switch_to_view("add_payment")
        if st.button(label="Histórico de Pagamentos"):
            st.write("Histórico de Pagamentos")


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

                    if payment_btn:
                        st.session_state["selected_student"] = student
                        switch_to_view("add_payment")
                    if detail_btn:
                        st.session_state["selected_student"] = student
                        switch_to_view("detail")

def view_students():

    if "view" in st.session_state:
        view = st.session_state['view']
        if view == "detail":
            detail_student()
        elif view == "add_payment":
            add_payment()

    else:
        list_students()
                                
                                