import requests
from cherrypy import request
from datetime import datetime
from modules.doctor.controller import Doctor
from modules.patient.controller import Patient
from modules.user.controller import User
from libraries.util import hash256, random_hash
from libraries.util import validate_password, validate_email
from collections import OrderedDict

class Common(object):

	def test(self):
		return {"status": 200, "data": {}, "message": "I'm working.", "access-key": random_hash()}

	def info(self):
		response = {"status": 200, "data": [], "message": "List of API's available", "access-key": random_hash()}

		response["data"].append(OrderedDict({
			"name": "Response",
			"description": "Basic API response structure.",
			"header": "Access-key which is used for next transaction.",
			"structure": {
				"status": "Http status code. Ex: [200, 400, ...]",
				"data": "DICT {} or LIST [] of info.",
				"message": "Description/message of the response.",
			}
		}))

		response["data"].append(OrderedDict({
			"name": "API list",
			"description": "List of all API's with their description.",
			"endpoint": "/api",
			"method": "GET",
			"arguments": {},
			"response": {}
		}))
		return response

	def patient_register(self, **params):
		response = {"status": 400, "data": {}, "message": "Unable to register patient.", "access-key": random_hash()}
		# Patient registration
		name = (request.params["name"]).strip()
		email = (request.params["email"]).strip()
		mobile = (request.params["mobile"]).strip()
		password = (request.params["password"]).strip()

		if len(name) < 3:
			response["message"] = "Invalid patient name."
		elif (not mobile.isdigit()) or (len(mobile) != 10):
			response["message"] = "Invalid mobile number."
		elif validate_email(email) == None:
			response["message"] = "Invalid email."
		elif validate_password(password) == None:
			response["message"] = "Invalid password. Should contain at least 1 number, 1 capital letter, 1 small-case letter and 1 special character from [@, #, %, &, $, ^, +]"
		else:
			patient = {
				"name": name,
				"email": email,
				"mobile": mobile,
				"password": hash256(str(password))
			}
			p = Patient()
			is_registered = p.register(patient)

			if is_registered["status"]:
				response = {"status": 200, "data": {}, "message": "Patient registration successful.", "access-key": random_hash()}
			else:
				response["message"] = is_registered["message"]
		return response

	def doctor_register(self, **params):
		response = {"status": 400, "data": {}, "message": "Unable to register doctor.", "access-key": random_hash()}
		# Doctor registration
		name = (request.params["name"]).strip()
		email = (request.params["email"]).strip()
		mobile = (request.params["mobile"]).strip()
		degree = (request.params["degree"]).strip()
		specialization = (request.params["specialization"]).strip()
		registration_number = (request.params["registration_number"]).strip()

		if len(name) < 3:
			response["message"] = "Invalid patient name."
		elif (not mobile.isdigit()) or (len(mobile) != 10):
			response["message"] = "Invalid mobile number."
		elif validate_email(email) == None:
			response["message"] = "Invalid email."
		elif len(registration_number) <= 4:
			response["message"] = "Invalid registration number."
		else:
			doctor = {
				"name": name,
				"email": email,
				"mobile": mobile,
				"degree": degree,
				"password": hash256(str(mobile)),
				"specialization": specialization,
				"registration_number": registration_number
			}
			d = Doctor()
			is_registered = d.register(doctor)

			if is_registered["status"]:
				response = {"status": 200, "data": {}, "message": "Doctor registered successfully.", "access-key": random_hash()}
			else:
				response["message"] = is_registered["message"]
		return response

	def login(self, **params):
		response = {"status": 400, "data": {}, "message": "Unable to login.", "access-key": random_hash()}
		# Login user by setting token.
		# print(request.headers["X-Access-Key"])
		username = (request.params["username"]).strip()
		password = (request.params["password"]).strip()

		if len(username) < 5:
			response["message"] = "Invalid username."
		elif (not username.isdigit()) and (validate_email(username) == None):
			response["message"] = "Invalid username."
		elif (username.isdigit()) and (len(username) != 10):
			response["message"] = "Invalid username."
		else:
			credentials = {
				"username": username,
				"password": hash256(str(password))
			}

			u = User()
			info = u.has_valid_credentials(credentials)
			if info["access_key"] is not None:
				response = {"status": 200, "data": info["data"], "message": "Successfully logged-in.", "access-key": info["access_key"]}
			else:
				response["message"] = "Invalid credentials."
		return response

	def logout(self, **params):
		# logout user session
		access_key = request.headers["X-Access-Key"]

		return {"status": 400, "data": {}, "message": "User logout", "access-key": random_hash()}

