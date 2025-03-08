import base64
import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # Load environment variables from .env

# Get credentials from .env
MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE')
MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')
MPESA_CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL')


def generate_access_token():
    stk_endpoint_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    credentials = f"{MPESA_CONSUMER_KEY}:{MPESA_CONSUMER_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {
            encoded_credentials
        }",
        "Content-Type": "application/json"

    }

    response = requests.get(stk_endpoint_url, headers=headers)
    access_token = json.loads(response.text)['access_token']
    print(access_token)
    try:
        response = requests.get(stk_endpoint_url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad status
        return response.json()['access_token']
    except Exception as e:
        print(f"Auth Error: {str(e)}")
        print(f"Response: {response.text}")
        return None
    print(access_token)
    return access_token



def sendStkPush():
    token = generate_access_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortCode = MPESA_SHORTCODE
    passkey = MPESA_PASSKEY
    callback = MPESA_CALLBACK_URL
    stk_password = base64.b64encode((shortCode + passkey + timestamp).encode('utf-8')).decode('utf-8')
        
        #choose one depending on you development environment
    url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
        
    requestBody = {
        "BusinessShortCode": shortCode,
        "Password": stk_password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerBuyGoodsOnline", #till "CustomerBuyGoodsOnline"
        "Amount": "10",
        "PartyA": "254721170527",
        "PartyB": shortCode,
        "PhoneNumber": "254721170527",
        "CallBackURL": callback,
        "AccountReference": "account",
        "TransactionDesc": "test"
    }
        
    try:
        response = requests.post(url, json=requestBody, headers=headers)
        print(response.json())
        return response.json()
    except Exception as e:
        print('Error:', str(e))

if __name__ == '__main__':
    try:
        generated_token = sendStkPush()
        print(generated_token)
    except Exception as e:
        print(f"Error: {str(e)}")