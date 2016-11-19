import sys
import requests
import hashlib
import json


url = 'http://127.0.0.1:8002/update/patient/basic'
# url = 'http://139.59.224.188:8002/update/patient/basic'

headers = {
    'X-ACCESS-KEY': '85bfbb2e88494e3b7dcd73b678f3928999724b96ecbfb336b2f2e6fa1ff56e85',
}

response = requests.post(url, params = {
		"id": 2,
		"name": "Goli Sunil",
		"gender": "M",
		"languages": "English, Kannada, Maithili, Goli",
		"dob": "14/11/1989",
		"blood_group": "A+"
	}, headers=headers)

print(response.headers)
print(response.text)
