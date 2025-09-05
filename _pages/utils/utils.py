from typing import Union
import streamlit as st
import streamlit_antd_components as sac


def switch_to_view(to_view: Union[str, None] = None) -> None:

    if to_view:
        st.session_state["view"] = to_view
    else:
        del st.session_state["view"]
    st.rerun()


def switch_to_view_button(message: str, to_view: Union[str, None] = None):
    with st.container():
        if st.button(message, use_container_width=True):
            switch_to_view(to_view)


@st.dialog(title="Mensagem")
def alert_dialog():
    sac.alert(label="Pagamento Finalizado!", icon="check-circle", color="success")
    switch_to_view_button("Retornar à lista de alunos")