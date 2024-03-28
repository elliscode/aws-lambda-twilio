import json
import http.client
import base64
import os
import urllib.parse

TWILIO_ACCT_SID = os.getenv('TWILIO_ACCT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
DEFAULT_MESSAGE_SENDER = os.getenv('DEFAULT_MESSAGE_SENDER')

def lambda_handler(event, context):
    print(json.dumps(event))

    if 'Records' not in event:
        return {
            'statusCode': 500,
            'status': 'invalid event supplied, requires a Records attribute',
        }
    
    try:
        for message in event['Records']:
            json_message = json.loads(message['body'])
            message_body = urllib.parse.quote(json_message['message'])
            message_recipient = urllib.parse.quote(json_message['phone'])
            message_sender = urllib.parse.quote(json_message.get('sender', DEFAULT_MESSAGE_SENDER))
            base64_encoded_auth = base64.b64encode(f'{TWILIO_ACCT_SID}:{TWILIO_AUTH_TOKEN}'.encode('utf-8')).decode('utf-8')
            conn = http.client.HTTPSConnection("api.twilio.com")
            payload = f'Body={message_body}&From={message_sender}&To={message_recipient}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {base64_encoded_auth}',
            }
            conn.request("POST", f"/2010-04-01/Accounts/{TWILIO_ACCT_SID}/Messages.json", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
        
        return {
            'statusCode': 200,
            'body': f'Sent messages'
        }
    except:
        pass
    finally:
        pass
        
    return {
        'statusCode': 500,
        'body': json.dumps('Something went wrong with sending the message')
    }