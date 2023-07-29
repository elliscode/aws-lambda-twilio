import json
import http.client
import base64
import os

TWILIO_ACCT_SID = os.getenv('TWILIO_ACCT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
DEFAULT_MESSAGE_SENDER = os.getenv('DEFAULT_MESSAGE_SENDER')

def lambda_handler(event, context):
    if 'Records' not in event:
        return {
            'statusCode': 500,
            'status': 'invalid event supplied, requires a Records attribute',
        }
    
    try:
        for message in event['Records']:
            json_message = json.loads(message['body'])
            message_body = json_message['message']
            message_recipient = json_message['phone']
            message_sender = json_message.get('sender', DEFAULT_MESSAGE_SENDER)
            base64_encoded_auth = base64.b64encode(f'{TWILIO_ACCT_SID}:{TWILIO_AUTH_TOKEN}'.encode('utf-8')).decode('utf-8')
            conn = http.client.HTTPSConnection("api.twilio.com")
            payload = f'Body={message_body}&From=%2B1{message_sender}&To=%2B1{message_recipient}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {base64_encoded_auth}',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
            }
            conn.request("POST", f"/2010-04-01/Accounts/{TWILIO_ACCT_SID}/Messages.json", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
        
        return {
            'statusCode': 200,
            'body': f'Sent messages'
        }
    finally:
        pass
        
    return {
        'statusCode': 500,
        'body': json.dumps('Something went wrong with sending the message')
    }