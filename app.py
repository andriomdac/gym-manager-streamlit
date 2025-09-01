import streamlit as st
import streamlit_antd_components as sac
from _pages.view_students import view_students
from _pages.add_student import add_student
from _pages.view_cash_registers import view_cash_registers
from icecream import ic


with st.sidebar.container():

    st.header("Gym Manager")

    menu = sac.menu(
        items=[
            sac.MenuItem(
                label="Painel (em breve)",
                icon="house",
                disabled=True
                ),
            sac.MenuItem(
                label="Matricular Aluno",
                icon="person-add"
            ),
            sac.MenuItem(
                label="Visualizar Alunos",
                icon="people"
            ),
            sac.MenuItem(
                label="Situação dos Aluno (em breve)",
                icon="exclamation-circle",
                disabled=True
            ),
            sac.MenuItem(
                label="Caixas Registradoras",
                icon="cash-stack",
            ),
        ],
        color="blue"
    )


with st.container():

    if menu == "Painel":
        pass

    if menu == "Matricular Aluno":
        add_student()

    if menu == "Visualizar Alunos":
        view_students()

    if menu == "Situação dos Aluno":
        pass
    if menu == "Caixas Registradoras":
        view_cash_registers()


ic(st.session_state.get("view"))