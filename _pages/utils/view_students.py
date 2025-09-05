import streamlit as st
import streamlit_antd_components as sac
from .utils import (
    switch_to_view,
    switch_to_view_button
)
from src.client import PaymentValueAPIClient


def student_detail_header(header: str, return_to_btn_msg: str, return_to_view: str):
    with st.container():
        col1, col2 = st.columns([2, 1], vertical_alignment="bottom")
        with col1:
            st.header(header)
        with col2:
            switch_to_view_button(message=return_to_btn_msg, to_view=return_to_view)


def student_detail_card(student: dict):
    col1, col2, col3 = st.columns([3, 3, 2])
    with col1:
        st.write(student["name"])
    with col2:
        st.write(student["reference"])
    with col3:
        st.write(student["phone"])


def new_payment_card(payment: dict):
    student = st.session_state['selected_student']

    with st.container():
        st.subheader(student["name"], divider=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            sac.tags(
                items=[
                    sac.Tag(
                        label=f"Data de Pagamento: {payment['payment_date']}",
                        icon='calendar',
                        color="blue"
                    ),
                    sac.Tag(
                        label=f"Pacote de Pagamento: {payment['payment_package']['name']}",
                        icon='calendar',
                        color="green"
                    ),
                    sac.Tag(
                        label=f"Data do Próx. Pagamento: {payment['next_payment_date']}",
                        icon='calendar',
                        color="orange",
                    ),
                ],
                size="lg",
                radius="sm",
            )
        with col2:
            with st.container():
                if payment['observations']:
                    st.warning(f"Obs:{payment["observations"] }")
    with st.container():
        payment_values_tags(payment=payment)
    with st.container():
        if st.button("Limpar Valores", type="secondary", use_container_width=True):
            value_client = PaymentValueAPIClient(student_id=student['id'], payment_id=payment['id'])
            response = value_client.delete_all_payment_values()
            if response.status_code == 204:
                st.success("Valores removidos com sucesso")
                st.rerun()
            


def payment_values_tags(payment: dict):
    st.write("Métodos: ")
    tags = []
    for value in payment.get('payment_values', ''):
        tags.append(
            sac.Tag(
                label=f"{value['method']}: R$ {value['value']:.2f}",
                icon="cash",
                color="green",
                size="lg",
                radius="sm",
                )
        )

    sac.tags(
        items=[tag for tag in tags]
    )