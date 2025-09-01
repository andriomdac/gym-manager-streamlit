import requests as req


BASE_URL = "http://localhost:8000/api/gyms/bd50151d-19f6-490b-bfcd-a21d50b3f8c8"


class StudentAPIClient():

    def __init__(self):
        self._base_url = f"{BASE_URL}/students"

    def get_students(self):
        return req.api.get(url=f"{self._base_url}/")
    
    def add_student(self, data: dict):
        return req.api.post(url=f"{self._base_url}/", json=data)

    def get_student(self, student_id: str):
        return req.api.get(url=f"{self._base_url}/{student_id}/")


class PaymentAPIClient():

    def __init__(self, student_id: str):
        self._base_url = f"{BASE_URL}/students/{student_id}"

    def get_payments(self):
        return req.api.get(url=f"{self._base_url}/payments/")
    
    def add_payment(self, data={}):
        return req.api.post(url=f"{self._base_url}/payments/", json=data)



class PaymentPackageAPIClient():

    def __init__(self):
        self._base_url = f"http://localhost:8000/api/payment-packages"
    
    def get_payment_packages(self):
        return req.api.get(url=f"{self._base_url}/")



class PaymentMethodAPIClient():

    def __init__(self):
        self._base_url = f"{BASE_URL}/payment-methods/"


class PaymentValueAPIClient():

    def __init__(self, student_id: str, payment_id: str):
        self._base_url = f"{BASE_URL}/students/{student_id}/payments/{payment_id}/values/"



class CashRegisterAPIClient():

    def __init__(self):
        self._base_url = f"{BASE_URL}/cash-registers/"

    def get_cash_registers(self):
        return req.api.get(url=f"{self._base_url}")

    def add_cash_register(self, data={}):
        return req.api.post(url=f"{self._base_url}", json=data)