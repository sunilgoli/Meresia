import sys
import requests
import hashlib
import json


url = 'http://127.0.0.1:8002/login'
# url = 'http://139.59.224.188:8002/login'

headers = {
    'X-ACCESS-KEY': 'f7e57489a2db37785d4833efc779f',
}

# Patient
# response = requests.post(url, params = {
# 		"username": "9972884232",
# 		"password": "9972884232"
# 	}, headers=headers)

# Doctor
response = requests.post(url, params = {
		"username": "8882884240",
		"password": "8882884240"
	}, headers=headers)
print(response.headers)
print(response.text)
