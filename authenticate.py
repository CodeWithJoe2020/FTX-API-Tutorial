#Authenticate to with User Credentials into the FTX Api

import time
import hmac
from requests import Request, Session, Response
import os
import json
from dotenv import load_dotenv
load_dotenv()

API_KEY_SECRET = os.getenv('API_KEY_SECRET')
API_KEY = os.getenv('API_KEY')


endpoint = 'https://ftx.com/api/account'


ts = int(time.time() * 1000)
request = Request('GET', 'https://ftx.com/api/account')
prepared = request.prepare()
s = Session()
signature_payload = f'{ts}{prepared.method}{prepared.path_url}'
if prepared.body:
    signature_payload += prepared.body
signature_payload = signature_payload.encode()
signature = hmac.new(API_KEY_SECRET.encode(), signature_payload, 'sha256').hexdigest()

prepared.headers['FTX-KEY'] = API_KEY
prepared.headers['FTX-SIGN'] = signature
prepared.headers['FTX-TS'] = str(ts)


response = s.send(prepared)
data = response.json()
print(data)
