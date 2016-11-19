import sys
import requests
import hashlib
import json


# url = 'http://127.0.0.1:8002/patient-registration'
url = 'http://139.59.224.188:8002/patient-registration'

headers = {
    'X-ACCESS-KEY': 'f7e57489a2db37785d4833efc779f',
}

response = requests.post(url, params = {
		"name": "Sunil Goli",
		"email": "gol1at2@goli.com",
		"mobile": "9912882332",
		"password": "Abc1234@"
	}, headers=headers)
print(response.text)
