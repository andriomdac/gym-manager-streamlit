import time
import streamlit as st
import streamlit_antd_components as sac
from src.client import CashRegisterAPIClient
from icecream import ic

register_client = CashRegisterAPIClient()


@st.dialog(title="Abrir Caixa")
def new_register():    
    if st.button("Hoje", use_container_width=True):
        new_register = register_client.add_cash_register()
        if new_register.status_code == 201:
            st.success("Caixa aberto com sucesso. Iniciando os trabalhos!")
            time.sleep(3)
            st.rerun()
        else:
            st.error(new_register.json())

    date_input = st.date_input(label="Outro dia", value=None)
    if date_input:
        new_register = register_client.add_cash_register(
            data={
                "register_date": date_input.strftime("%Y-%m-%d")
                }
        )
        if new_register.status_code == 201:
            st.success("Caixa criado com sucesso.")
            time.sleep(2)
            st.rerun()
        else:
            st.error(new_register.json())


@st.dialog(title="Fechar Caixa?")
def close_register_dialog():
    with st.container():
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Fechar", type="primary", use_container_width=True):
                pass
        with col2:
            if st.button("Cancelar", use_container_width=True):
                st.rerun()


def view_cash_registers():
    registers_list = register_client.get_cash_registers().json()

    with st.container():
        col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
        with col1:
            st.header("Caixas Registradoras")
        with col2:
            if st.button(label="Abrir Caixa", use_container_width=True):
                new_register()

    for register in registers_list:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1], vertical_alignment="center")
            with col1:
                st.info(register["register_date"])
                st.success(f"R$ {register['amount']}")

            with col2:
                if st.button(
                    label="detalhes",
                    use_container_width=True,
                    key=f"detail - {register['id']}"
                    ):
                    pass
                if st.button(
                    label="Fechar",
                    use_container_width=True,
                    type="primary",
                    key=f"close - {register['id']}"
                    ):
                    close_register_dialog()
