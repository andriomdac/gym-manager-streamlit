import streamlit as st
import requests as req

S_BASE_URL = "http://localhost:8000/api/gyms/bd50151d-19f6-490b-bfcd-a21d50b3f8c8"
BASE_URL = "http://localhost:8000/api"


def get_headers():
    return {
        'Authorization': f"Bearer {st.session_state['token']}",
        'Content-Type': 'application/json'
    }


class TokenAPIClient():
    
    def __init__(self):
        self._base_url = f"{BASE_URL}/token/"
    
    def _get_headers(self):
        return get_headers()
    
    def get_token(self, username: str, password: str):
        return req.api.post(
            url=self._base_url,
            json={
                "username": username,
                "password": password
                },
            headers=self._get_headers()
            )
        
    def refresh_token(self, refresh_token: str):
        return req.api.post(
            url=f"{self._base_url}/refresh/",
            json={"refresh": refresh_token},
            headers=self._get_headers()
        )
        
    def verify_token(self, token: str):
        return req.api.post(
            url=f"{self._base_url}/verify/",
            json={"token": token},
            headers=self._get_headers()
        )
        


class StudentAPIClient():

    def __init__(self):
        self._base_url = f"{S_BASE_URL}/students"

    def _get_headers(self):
        return get_headers()

    def get_students(self):
        return req.api.get(
            url=f"{self._base_url}/",
            headers=self._get_headers()
            )
    
    def add_student(self, data: dict):
        return req.api.post(
            url=f"{self._base_url}/",
            json=data,
            headers=self._get_headers()
            )

    def get_student(self, student_id: str):
        return req.api.get(
            url=f"{self._base_url}/{student_id}/",
            headers=self._get_headers()
            )


class PaymentAPIClient():

    def __init__(self, student_id: str):
        self._base_url = f"{S_BASE_URL}/students/{student_id}"

    def _get_headers(self):
        return get_headers()

    def get_payments(self):
        return req.api.get(
            url=f"{self._base_url}/payments/",
            headers=self._get_headers()
            )

    def get_payment(self, payment_id: str):
        return req.api.get(
            url=f"{self._base_url}/payments/{payment_id}/",
            headers=self._get_headers()
            )
    
    def add_payment(self, data={}):
        return req.api.post(
            url=f"{self._base_url}/payments/",
            json=data,
            headers=self._get_headers()
            )

    def delete_payment(self, payment_id: str):
        return req.api.delete(
            url=f"{self._base_url}/payments/{payment_id}/",
            headers=self._get_headers()
            )


class PaymentPackageAPIClient():

    def __init__(self):
        self._base_url = f"http://localhost:8000/api/payment-packages"

    def _get_headers(self):
        return get_headers()
    
    def get_payment_packages(self):
        return req.api.get(
            url=f"{self._base_url}/",
            headers=self._get_headers()
            )


class PaymentMethodAPIClient():

    def __init__(self):
        self._base_url = f"http://localhost:8000/api/payment-methods/"

    def _get_headers(self):
        return get_headers()

    def get_methods(self):
        return req.api.get(
            url=self._base_url,
            headers=self._get_headers()
            )


class PaymentValueAPIClient():

    def __init__(self, student_id: str, payment_id: str):
        self._base_url = f"{S_BASE_URL}/students/{student_id}/payments/{payment_id}/values/"

    def _get_headers(self):
        return get_headers()

    def get_payment_values(self):
        return req.api.get(
            url=f"{self._base_url}",
            headers=self._get_headers()
            )
    
    def add_payment_value(self, data: dict={}):
        return req.api.post(
            url=f"{self._base_url}",
            json=data,
            headers=self._get_headers()
            )
    
    def delete_all_payment_values(self):
        return req.api.delete(
            url=f"{self._base_url}delete/",
            headers=self._get_headers()
            )


class CashRegisterAPIClient():

    def __init__(self):
        self._base_url = f"{S_BASE_URL}/cash-registers/"

    def _get_headers(self):
        return get_headers()

    def get_cash_registers(self):
        return req.api.get(
            url=f"{self._base_url}",
            headers=self._get_headers()
            )

    def add_cash_register(self, data={}):
        return req.api.post(
            url=f"{self._base_url}",
            json=data,
            headers=self._get_headers()
            )
