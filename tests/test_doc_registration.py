import sys
import requests
import hashlib
import json


# url = 'http://127.0.0.1:8002/doctor-registration'
url = 'http://139.59.224.188:8002/doctor-registration'

headers = {
    'X-ACCESS-KEY': 'f7e57489a2db37785d4833efc779f',
}

response = requests.post(url, params = {
		"name": "Sunil Goli Doc",
		"email": "eolc@goli.com",
		"mobile": "8882884240",
		"specialization": "Cardiologist",
		"degree": "MBBS, MD",
		"registration_number": "PIR1285"
	}, headers=headers)
print(response.text)
