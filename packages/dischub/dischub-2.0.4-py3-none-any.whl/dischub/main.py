import requests
class Dischub:
    def __init__(self):
        self.api_url = "https://dischub.co.zw/api/orders/create/"
    def create_payment(self, data):
        required_keys = {'sender', 'recipient', 'amount', 'currency'}
        try:
            if all(key in data and data[key] for key in required_keys):
                response = requests.post(self.api_url, json=data)
                if response.status_code == 201:
                    return {'Status': 'Success', 'Message': 'Payment initiated', 'Response_code': 201}
                else:
                    return {
                        'Status': 'Failure',
                        'Message': f"Payment failed with status code {response.status_code}",
                        'Response_code': response.status_code,
                        'Details': response.text
                    }
            else:
                return {'Status': 'Bad request', 'Message': 'Missing or empty required fields', 'Response_code': 400}
        except requests.exceptions.RequestException as e:
            return {'Status': 'Error', 'Message': str(e)}
