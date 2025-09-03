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
from icecream import ic


st.set_page_config(page_title="view_students")


def switch_to_view(to_view: Union[str, None] = None) -> None:

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


def new_payment_card(payment: dict):
    student = st.session_state['selected_student']

    with st.container():
        st.subheader(student["name"])

        col1, col2 = st.columns(2)
        with col1:
            sac.tags(
                items=[
                    sac.Tag(
                        label=f"Data de Pagamento: {payment['payment_date']}",
                        icon='calendar',
                        color="blue"
                    ),
                    sac.Tag(
                        label=f"Pacote de Pagamento: {payment['payment_package']}",
                        icon='calendar',
                        color="green"
                    ),
                    sac.Tag(
                        label=f"Data do Próx. Pagamento: {payment['next_payment_date']}",
                        icon='calendar',
                        color="orange"
                    ),
                ],
                size="md"
            )
        with col2:
            with st.container(border=True):
                value_client = PaymentValueAPIClient(
                    student_id=student['id'],
                    payment_id=payment['id']
                    )
                st.write("Métodos: ")


    with st.container(border=True):
        if payment['observations']:
            st.info(f"Obs:{payment["observations"] }")


def add_value():
    student = st.session_state['selected_student']
    payment = st.session_state['selected_payment']
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

            submit = st.form_submit_button(label="Adicionar", use_container_width=True)
            if submit:
                value_client = PaymentValueAPIClient(
                    student_id=student['id'],
                    payment_id=payment['id']
                    )
                response = value_client.add_payment_value(data=data)
                if response.status_code == 201:
                    st.success(f"{response.json()}")
                else:
                    st.error(f"{response.json()}")


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
                    st.session_state["selected_payment"] = new_payment.json()
                    st.session_state["selected_payment"]["payment_package"] = payment_package_input
                    switch_to_view("add_value")
                st.info(new_payment.json())


def student_detail_header(header: str, return_to_btn_msg: str, return_to_view: str):
    with st.container():
        col1, col2 = st.columns([2, 1], vertical_alignment="bottom")
        with col1:
            st.header(header)
        with col2:
            switch_to_view_button(message=return_to_btn_msg, to_view=return_to_view)


def payment_values_tags(payment: dict):
    st.write("Métodos: ")
    tags = []
    for value in payment['payment_values']:
        tags.append(
            sac.Tag(
                label=f"{value['method']}: {value['value']}",
                icon="cash",
                color="green",
                size="lg",
                radius="sm",
                )
        )

    sac.tags(
        items=[tag for tag in tags]
    )


def payments_history():
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
        elif view == "add_value":
            add_value()
        elif view == "payments_history":
            payments_history()

    else:
        list_students()
                                
                                