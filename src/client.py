import requests as req


BASE_URL = "http://localhost:8000/api/gyms/bd50151d-19f6-490b-bfcd-a21d50b3f8c8"


class StudentAPIClient():

    def __init__(self):
        self._base_url = f"{BASE_URL}/students/"

    def get_students(self):
        return req.api.get(url=self._base_url)
    
    def add_students(self, data: dict):
        return req.api.post(url=self._base_url, json=data)


class PaymentAPIClient():

    def __init__(self, student_id: str):
        self._base_url = f"{BASE_URL}/students/{student_id}"



class PaymentPackageAPIClient():

    def __init__(self):
        self._base_url = f"{BASE_URL}/payment-packages/"



class PaymentMethodAPIClient():

    def __init__(self):
        self._base_url = f"{BASE_URL}/payment-methods/"



class PaymentValueAPIClient():

    def __init__(self, student_id: str, payment_id: str):
        self._base_url = f"{BASE_URL}/students/{student_id}/payments/{payment_id}/values/"
