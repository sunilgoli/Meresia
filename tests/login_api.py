import sys
import requests
import hashlib
import json

data_hash = ("0b89a3403fade70a621573b58f9fac9ea83" + "Goli").encode('utf-8')
hash = hashlib.sha1(data_hash).hexdigest()

# url = 'http://127.0.0.1:8002/login'
url = 'http://139.59.224.188:8002/login'

headers = {
    'X-ACCESS-KEY': API_ACCESS_KEY,
    'X-HASH': hash
}

data = json.dumps({"username": "Goli", "password": "Goli 1488"})
response = requests.post(url, params = {"username": "Goli", "password": "Goli 1488"}, headers=headers)
print(response.text)
