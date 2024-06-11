import requests
import hmac
import hashlib
import time
import json

# Define your API credentials
api_key = '00ed545e-1998-425f-b460-f733525cb2ca'
secret_key = 'E51EF821DD0A6B5B0E824859969AB6D6'
passphrase = 'Maxym20045*'



def create_signature(timestamp, method, request_path, body, secret_key):
    message = f'{timestamp}{method}{request_path}{body}'
    signature = hmac.new(bytes(secret_key, 'utf-8'), bytes(message, 'utf-8'), hashlib.sha256).digest()
    return signature


p
def get_timestamp():
    return str(int(time.time()))



def get_spot_balance():
    url = 'https://www.okx.com/api/v5/account/balance'
    method = 'GET'
    request_path = '/api/v5/account/balance'
    body = ''

    timestamp = get_timestamp()
    signature = create_signature(timestamp, method, request_path, body, secret_key)

    headers = {
        'OK-ACCESS-KEY': api_key,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': passphrase,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.text



balance = get_spot_balance()
print(json.dumps(balance, indent=2))
