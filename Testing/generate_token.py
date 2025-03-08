import base64
import json
import requests
from datetime import datetime

def generate_access_token():
    consumer_key = "8hzJOzdKUBJGIcdtwyd4O74CujPLGrVybGtnFFOMkseNW7DS"
    consumer_secret = "SVlR8ZTqRR3F4AvzmA2DtpHlABSHsyISXx9BEgxu1F2iF8A1he3zgVMQLNjLW41i"

    #choose one depending on you development environment
    #live
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    try:
        
        encoded_credentials = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()

        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

        # Send the request and parse the response
        response = requests.get(url, headers=headers).json()

        # Check for errors and return the access token
        if "access_token" in response:
            print(response["access_token"])
            return response["access_token"]
        else:
            raise Exception("Failed to get access token: " + response["error_description"])
    except Exception as e:
        raise Exception("Failed to get access token: " + str(e)) 



def sendStkPush():
        token = generate_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        shortCode = "174379" #sandbox -174379
        passkey = "4c849cd0981171099907fdd0c323de0ae69782b5fc4402e9beab7cb00910526"
        stk_password = base64.b64encode((shortCode + passkey + timestamp).encode('utf-8')).decode('utf-8')
        callback = "https://ac62-41-139-218-67.ngrok-free.app/manager/mpesa/callback/"
        
        #choose one depending on you development environment
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
        
        requestBody = {
            "BusinessShortCode": shortCode,
            "Password": stk_password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline", #till "CustomerBuyGoodsOnline"
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
            return None

if __name__ == "__main__":
    try:
        generated_token = sendStkPush()
        print(generated_token)
    except Exception as e:
        print(f"Error: {str(e)}")