import sys
import requests
import hashlib
import json


# url = 'http://127.0.0.1:8002/update/doctor/clinic'
url = 'http://139.59.224.188:8002/update/doctor/clinic_id'

# headers = {
#     'X-ACCESS-KEY': '85bfbb2e88494e3b7dcd73b678f3928999724b96ecbfb336b2f2e6fa1ff56e85',
# }

# response = requests.get(url, params = {
# 		"id": 2
# 	},

headers = {
    'X-ACCESS-KEY': '094905ec7a96e18f3bf3add3f8b461cd1debac44cb52f4c4b43e669a9e5a47a1',
}

response = requests.post(url, params = {
		"id": 9,
		"clinic_id": 4,
		"hospital": "NRM",
		"city": "Bangalore",
		"state": "Karnataka",
		"pincode": "560078",
		"start_date": "14/11/1988",
		"end_date": "",

	}, headers=headers)

print(response.headers)
print(response.text)
