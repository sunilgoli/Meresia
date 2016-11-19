import random
import requests
import sys
import re
import uuid
from datetime import datetime, timedelta
import simplejson as json
import collections
import hashlib
from config.constants import HASH_KEY


def generate_token(id):
	# Generate a random string for token
	uid = uuid.uuid4()
	return hash256(uid.hex + str(id))


def validate_email(email):
	# Validate email pattern
	return re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)


def validate_password(password):
	# Validate password pattern
	# regx = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{6,}$')
	regx = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[@#%&$^+])[A-Za-z\d@#%&$^+]{6,}$')
	return regx.match(password)


def random_hash():
	# Generate a random hash
	return random.getrandbits(128)


def hash256(string):
	# Generate a hash of the string with system hash key
	hash_inst = hashlib.sha256((string + HASH_KEY).encode('utf-8'))
	return hash_inst.hexdigest()


def object_to_list(attribute, data_object):
	"""
		Build a list from object(data_object) with the values for the given
		attribute_list(properties of the data object whose value need to be fetched)
	"""
	return [(getattr(obj, attribute)) for obj in data_object]


def object_to_dict(attribute_list, data_object):
	"""
		Build a Directory from object(data_object) with the values for the given attribute_list (properties of the data object whose value need to be fetched)
	"""
	return {attribute: str(getattr(data_object, attribute)) for attribute in attribute_list}


def object_to_dict_with_key_and_value(key, value, data_object):
	"""
		Build a dict with given key and value attributes from data_object and sort dict wrt key.
	"""
	return collections.OrderedDict(sorted(({str(getattr(obj, key)): getattr(obj, value) for obj in data_object}).items()))


def object_to_list_of_dicts(attribute_list, data_object):
	"""
		Build a List of directories from object(data_object) with the values for the given attribute_list(properties of the data object whose value need to be fetched)
	"""
	return [object_to_dict(attribute_list, obj) for obj in data_object]


def object_to_dict_with_key(key, data_object):
	response = {}
	try:
		for obj in data_object:
			response[getattr(obj, key)] = obj
	except Exception as e:
		print(e)
	return response


class JSONEncoder(json.JSONEncoder):
	"""
		Json converter
	"""
	"""Custom JSON encoder to handle datetime serialization"""
	def default(self, obj):
		if isinstance(obj, datetime):
			return obj.strftime("%Y-%m-%d %H:%M:%S")
		return json.JSONEncoder.default(self, obj)


def post_api_response(api, params=''):
	"""
		Post API response
	"""
	response = requests.post(api, params) if params else requests.post(api)
	if response:
		return response.json()
	else:
		return {}


def get_api_response(api):
	"""
		Get API response
	"""
	response = requests.post(api)
	if response:
		return response.json()
	else:
		return {}


def previous_date(current_date, previous_days):
	"""
		Get date for the previous n'th day.
	"""
	return current_date - timedelta(days=previous_days)


def future_date(current_date, future_days):
	"""
		Get date for the up coming n'th day.
	"""
	return current_date + timedelta(days=future_days)

