import sys
import requests
import hashlib
import json


url = 'http://127.0.0.1:8002/update/doctor/basic'
# url = 'http://139.59.224.188:8002/update/doctor/basic'

headers = {
    'X-ACCESS-KEY': '85bfbb2e88494e3b7dcd73b678f3928999724b96ecbfb336b2f2e6fa1ff56e85',
}

response = requests.post(url, params = {
		"id": 2,
		"doc_type": "Basic Details",
		"email": "sunil@patient.com",
		"address_line_1": "123 derfet",
		"address_line_2": "address line 3",
		"address_line_3": "",
		"area": "JP nager",
		"pincode": "56078",
		"state": "Karnataka",
		"city": "Bangalore",
		"country": "India"
	}, headers=headers)

print(response.headers)
print(response.text)
