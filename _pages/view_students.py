from typing import Union
import streamlit as st
import streamlit_antd_components as sac
from src.client import (
    StudentAPIClient,
    PaymentAPIClient,
    PaymentPackageAPIClient,
    PaymentValueAPIClient,
    PaymentMethodAPIClient
    )
from .utils.utils import (
    switch_to_view,
    switch_to_view_button,
    alert_dialog
    )
from .utils.view_students import (
    student_detail_card,
    new_payment_card,
    student_detail_header,
    payment_values_tags
)
from icecream import ic


st.set_page_config(page_title="view_students")


class ViewStudentPage:
    def add_value(self):
        student = st.session_state['selected_student']
        session_payment = st.session_state['selected_payment']
        payment = PaymentAPIClient(student_id=student['id']).get_payment(payment_id=session_payment['id']).json()

        with st.container():
            col1, col2 = st.columns([2, 1], vertical_alignment="bottom")
            with col1:
                st.header("Métodos de Pagamento")
            with col2:
                switch_to_view_button(message="<- Voltar aos detalhes", to_view="detail")
        
        with st.container(border=True):
            new_payment_card(payment=payment)

        with st.container():
            with st.form(key="add_value"):
                col1, col2 = st.columns(2)
                with col1:
                    method_client = PaymentMethodAPIClient()
                    methods = method_client.get_methods().json()

                    method_names = [method['name'] for method in methods]
                    method_id_mapping = {method['name']: method['id'] for method in methods}

                    method_input = st.selectbox(label="Método", options=method_names)
                    method_input = method_id_mapping[method_input]
                with col2:
                    value_input = st.number_input(label="Valor recebido")
                
                data = {}
                data['value'] = value_input
                data['payment_method'] = method_input

                add_value = st.form_submit_button(label="Adicionar", use_container_width=True)
                finish = st.form_submit_button(label="Concluir Pagamento", use_container_width=True)
                if add_value:
                    value_client = PaymentValueAPIClient(
                        student_id=student['id'],
                        payment_id=payment['id']
                        )
                    response = value_client.add_payment_value(data=data)
                    if response.status_code == 201:
                        st.success(f"{response.json()}")
                        st.rerun()
                    else:
                        st.error(f"{response.json()}")
                if finish:
                    @st.dialog("Mensagem")
                    def finish_dialog():
                        sac.alert(label="Pagamento Finalizado!", icon="check-circle", color="success")
                        switch_to_view_button("Retornar à lista de alunos")
                    finish_dialog()


    def add_payment(self):
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
            payment_client = PaymentAPIClient(student_id=student["id"])
            p_packages_client = PaymentPackageAPIClient()

            with st.form(key="add_payment", enter_to_submit=True):
                col1, col2 = st.columns(2)
                payment_packages = p_packages_client.get_payment_packages().json()
                
                # Map dos pacotes de pagamento
                package_names = [package["name"] for package in payment_packages]
                package_id_mapping = {
                    package["name"]: package["id"] for package in payment_packages
                    }
                with col1:    
                    payment_package_input = st.selectbox(
                        label="Pacote de Pagamento",
                        options=package_names
                        )
                    package_id = package_id_mapping[payment_package_input]
                with col2:
                    observations = st.text_input("Observações")

                submit = st.form_submit_button(label="Próximo", use_container_width=True)
                if submit:
                    data = {}
                    data['payment_package'] = package_id
                    data['observations'] = observations
                    new_payment = PaymentAPIClient(student_id=student["id"]).add_payment(data=data)
                    if new_payment.status_code == 201:
                        new_payment = new_payment.json()
                        new_payment = payment_client.get_payment(new_payment['id'])
                        st.session_state["selected_payment"] = new_payment.json()
                        st.session_state["selected_payment"]["payment_package"] = payment_package_input
                        switch_to_view("add_value")
                    st.info(new_payment.json())


    def payments_history(self):
        student = st.session_state["selected_student"]
        payments_client = PaymentAPIClient(student_id=student['id'])
        with st.container():
            student_detail_header(
                header="Histórico de Pagamentos",
                return_to_btn_msg="<- Voltar aos Detalhes",
                return_to_view="detail"        
                )
        with st.container(border=True):
            student_detail_card(student=student)
        with st.container():
            payments = payments_client.get_payments().json()

            for payment in payments:
                payment_date = payment["payment_date"]
                next_payment_date = payment["next_payment_date"]
                payment_package = payment["payment_package"]["name"]


                with st.container(border=True):
                    st.subheader(payment["created_at"], divider=True)
                    sac.tags(
                        items=[
                            sac.Tag(
                                label=f"Data de Pagamento: {payment_date}",
                                icon="calendar-check",
                                color="geekblue",
                            ),
                            sac.Tag(
                                label=f"Pacote de Pagamento: {payment_package}",
                                icon="box2",
                                color="orange"
                            ),
                            sac.Tag(
                                label=f"Próximo Pagamento: {next_payment_date}",
                                icon="calendar",
                                color="magenta"
                            ),
                        ],
                        direction="horizontal",
                        size="lg",
                        radius="sm",
                    )
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        payment_values_tags(payment=payment)
                    with col2:
                        if st.button(label="Excluir", type="primary", use_container_width=True):
                            response = payments_client.delete_payment(payment_id=payment['id'])
                            if response.status_code == 204:
                                st.success("Deletado")
                                st.rerun()
                            else:
                                st.error(f"{response.content}")


    def detail_student(self):
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
            options = sac.buttons(
                items=[
                    sac.ButtonsItem(
                        icon="arrow-right",
                        color="blue",
                    ),
                    sac.ButtonsItem(
                        label="Adicionar Pagamento",
                        icon="plus",
                        color="green",
                    ),
                    sac.ButtonsItem(
                        label="Histórico de Pagamentos",
                        icon="clock-history",
                        color="orange"
                    ),
                ],
                variant="filled",
                use_container_width=True
            )
            if options == "Adicionar Pagamento":
                switch_to_view("add_payment")
            elif options == "Histórico de Pagamentos":
                switch_to_view("payments_history")


    def list_students(self):
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
    student_page = ViewStudentPage()
    if "view" in st.session_state:
        view = st.session_state['view']
        if view == "detail":
            student_page.detail_student()
        elif view == "add_payment":
            student_page.add_payment()
        elif view == "add_value":
            student_page.add_value()
        elif view == "payments_history":
            student_page.payments_history()

    else:
        student_page.list_students()           