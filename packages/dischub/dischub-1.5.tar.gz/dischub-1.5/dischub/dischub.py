import requests
#import webbrowser
class Dischub:
    def __init__(self):
        self.api_url = "http://10.76.225.90:8000/api/orders/create/"
    def create_payment(self, data):
        required_keys = {'sender', 'recipient', 'amount', 'currency'}
        try:
            if all(key in data and data[key] for key in required_keys):
                requests.post(self.api_url, json=data)
                #recipient_value = data["recipient"]
                #redirect_url = f"http://10.76.225.90:8000/api/make/payment/to/{recipient_value}"
                #webbrowser.open(redirect_url)
                return {'Status': 'Success', 'Message': 'Payment initiated', 'Response_code': 201}
            else:
                return {'Status': 'Bad request', 'Message': 'Payment failed to initiate', 'Response_code': 400}
        except requests.exceptions.RequestException as e:
            return {'status': 'error', 'message': str(e)}


class Dischub:
    def __init__(self):
        self.api_url = "http://10.76.225.90:8000/api/orders/create/"
    def create_payment(self):
        data = {'sender', 'recipient', 'amount', 'currency'}
        requests.post(self.api_url, json=data)