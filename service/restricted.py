from cherrypy import request
from datetime import datetime

from config.constants import MIN_AGE
from config.constants import GENDER
from config.constants import LANGUAGES
from config.constants import SPECIALTIES
from config.constants import PATIENT_DOCUMENTS
from config.constants import BLOOD_GROUP

from libraries.util import validate_password
from libraries.util import validate_email
from libraries.util import random_hash

from modules.user.controller import User
from modules.doctor.controller import Doctor
from modules.patient.controller import Patient

import json


class Service(object):

	def test(self, **params):
		return {"status": 200, "data": {}, "message": "I'm working.", "access-key": random_hash()}

	def basic(self,  **params):
		user_id = (request.params["id"]).strip()
		token = request.headers["X-Access-Key"]
		response = {"status": 400, "data": {}, "message": "Invalid access.", "access-key": token}
		u = User()
		instance = u.is_valid_token(token, user_id)

		if instance:
			response["status"] = 200
			response["message"] = "Doctor info"
			response["data"] = u.info(instance)
		return response

	def update_doctor_basic(self, **params):
		token = request.headers["X-Access-Key"]
		response = {"status": 400, "data": {}, "message": "Invalid access.", "access-key": token}
		try:
			user_id = (request.params["id"]).strip()
			name = (request.params["name"]).strip()
			degree = (request.params["degree"]).strip()
			gender = (request.params["gender"]).strip()
			experience = (request.params["experience"]).strip()
			languages = (request.params["languages"]).strip()
			specialties = (request.params["specialties"]).strip()
			dob = (request.params["dob"]).strip()
			languages = [x.strip() for x in languages.split(",")]
			specialties = [x.strip() for x in specialties.split(",")]

			for l in languages:
				if l not in LANGUAGES:
					languages.remove(l)

			for s in specialties:
				if s not in SPECIALTIES:
					specialties.remove(s)

			u = User()
			instance = u.is_valid_token(token, user_id)
			if instance:
				# Valid user
				if len(name) < 3:
					response["message"] = "Invalid name."
				elif len(dob) != 10:
					response["message"] = "Invalid date of birth."
				elif len(degree) < 3:
					response["message"] = "Invalid degree."
				elif len(languages) < 3:
					response["message"] = "Invalid language."
				elif len(specialties) < 3:
					response["message"] = "Invalid specialties."
				elif gender not in GENDER:
					response["message"] = "Invalid gender."
				elif not experience.isdigit():
					response["message"] = "Invalid experience."
				elif not languages:
					response["message"] = "Invalid language."
				elif not specialties:
					response["message"] = "Invalid specialty."
				else:

					data = {
						"user_id": user_id,
						"name": name,
						"degree": degree,
						"gender": gender,
						"experience": experience,
						"languages": languages,
						"specialties": specialties,
						"dob": datetime.strptime(dob, "%d/%m/%Y").date()
					}
					d = Doctor()
					is_updated = d.update_basic(data, instance)

					if is_updated:
						response["status"] = 200
						response["message"] = "Successfully updated."
					else:
						response["message"] = "Unable updated."
		except Exception as e:
			print(e)
			response["message"] = str(e)
		return response

	def update_doctor_contact(self, **params):
		token = request.headers["X-Access-Key"]
		response = {"status": 400, "data": {}, "message": "Invalid access.", "access-key": token}
		try:
			user_id = (request.params["id"]).strip()
			mobile = (request.params["mobile"]).strip()
			email = (request.params["email"]).strip()
			address_line_1 = (request.params["address_line_1"]).strip()
			address_line_2 = (request.params["address_line_2"]).strip()
			address_line_3 = (request.params["address_line_3"]).strip()
			area = (request.params["area"]).strip()
			pincode = (request.params["pincode"]).strip()
			state = (request.params["state"]).strip()
			city = (request.params["city"]).strip()
			country = (request.params["country"]).strip()

			u = User()
			instance = u.is_valid_token(token, user_id)
			if instance:
				# Valid user
				if (not mobile.isdigit()) or (len(mobile) != 10):
					response["message"] = "Invalid mobile number."
				elif validate_email(email) == None:
					response["message"] = "Invalid email."
				elif len(address_line_1) < 3:
					response["message"] = "Invalid address line."
				elif len(area) < 3:
					response["message"] = "Invalid area."
				elif (len(pincode) < 5) and (not pincode.isdigit()):
					response["message"] = "Invalid pin-code."
				elif not state:
					response["message"] = "Invalid state."
				elif not city:
					response["message"] = "Invalid city."
				elif not country:
					response["message"] = "Invalid country."
				else:
					data = {
						"user_id": user_id,
						"mobile": mobile,
						"email": email,
						"address_line_1": address_line_1,
						"address_line_2": address_line_2,
						"address_line_3": address_line_3,
						"area": area,
						"pincode": pincode,
						"state": state,
						"city": city,
						"country": country
					}
					d = Doctor()
					is_updated = d.update_contact(data, instance)

					if is_updated:
						response["status"] = 200
						response["message"] = "Successfully updated."
					else:
						response["message"] = "Unable updated."

		except Exception as e:
			print(e)
			response["message"] = str(e)
		return response

	def update_consultation(self, **params):
		token = request.headers["X-Access-Key"]
		response = {"status": 400, "data": {}, "message": "Invalid access.", "access-key": token}
		try:
			user_id = (request.params["id"]).strip()
			call = (request.params["call"]).strip()
			video = (request.params["video"]).strip()
			mail = (request.params["mail"]).strip()
			chat = (request.params["chat"]).strip()
			appointment = (request.params["appointment"]).strip()

			u = User()
			instance = u.is_valid_token(token, user_id)
			if instance:
				# Valid user
				if call and (not call.isdigit()):
					call = None
				if video and (not video.isdigit()):
					video = None
				if mail and (not mail.isdigit()):
					mail = None
				if (not chat) or (not chat.isdigit()):
					chat = None
				if appointment and (not appointment.isdigit()):
					appointment = None

				data = {
					"Call": call,
					"Video": video,
					"Mail": mail,
					"Chat": chat,
					"Appointment": appointment
				}

				d = Doctor()
				is_updated = d.update_consultation(data, instance)

				if is_updated:
					response["status"] = 200
					response["message"] = "Successfully updated."
				else:
					response["message"] = "Unable updated."

		except Exception as e:
			print(e)
			response["message"] = str(e)
		return response

	def update_doctor_clinic(self, **params):
		token = request.headers["X-Access-Key"]
		response = {"status": 400, "data": {}, "message": "Invalid access.", "access-key": token}
		try:
			user_id = (request.params["id"]).strip()
			clinic_id  = (request.params["clinic_id"]).strip()
			hospital  = (request.params["hospital"]).strip()
			city  = (request.params["city"]).strip()
			state  = (request.params["state"]).strip()
			pincode  = (request.params["pincode"]).strip()
			start_date  = (request.params["start_date"]).strip()
			end_date  = (request.params["end_date"]).strip()

			u = User()
			instance = u.is_valid_token(token, user_id)
			if instance:
				if not hospital:
					response["message"] = "Hospital/Clinic name required."
				elif not city:
					response["message"] = "City required."
				elif not state:
					response["message"] = "State required."
				elif not pincode:
					response["message"] = "Pincode required."
				elif not pincode.isdigit():
					response["message"] = "Invalid pincode."
				elif not start_date:
					response["message"] = "Start date required."
				else:
					start_date = datetime.strptime(start_date, "%d/%m/%Y").date()
					end_date = datetime.strptime(end_date, "%d/%m/%Y").date() if end_date else None
					data = {
						"user_id": user_id,
						"clinic_id": int(clinic_id),
						"hospital": hospital,
						"city": city,
						"state": state,
						"pincode": pincode,
						"start_date": start_date,
						"end_date": end_date
					}
					d = Doctor()
					is_updated = d.update_clinic(data, instance)

					if is_updated:
						response["status"] = 200
						response["message"] = "Successfully updated."
					else:
						response["message"] = "Unable updated."

		except Exception as e:
			print(e)
			response["message"] = str(e)
		return response

	def doctor_clinic(self, **params):
		token = request.headers["X-Access-Key"]
		response = {"status": 400, "data": {}, "message": "Invalid access.", "access-key": token}
		try:
			user_id = (request.params["id"]).strip()
			u = User()
			instance = u.is_valid_token(token, user_id)
			if instance:
				d = Doctor()
				response["status"] = 200
				response["message"] = "List of doctor clinics."
				response["data"] = d.clinics(instance)
		except Exception as e:
			print(e)
			response["message"] = str(e)
		return response

	def doctor_pricing(self, **params):
		token = request.headers["X-Access-Key"]
		response = {"status": 400, "data": {}, "message": "Invalid access.", "access-key": token}
		try:
			user_id = (request.params["id"]).strip()
			u = User()
			instance = u.is_valid_token(token, user_id)
			if instance:
				d = Doctor()
				response["status"] = 200
				response["message"] = "List of doctor pricing."
				response["data"] = d.pricing(instance)
		except Exception as e:
			print(e)
			response["message"] = str(e)
		return response

	def update_patient_basic(self, **params):
		token = request.headers["X-Access-Key"]
		response = {"status": 400, "data": {}, "message": "Invalid access.", "access-key": token}
		try:
			user_id = (request.params["id"]).strip()
			name = (request.params["name"]).strip()
			gender = (request.params["gender"]).strip()
			languages = (request.params["languages"]).strip()
			dob = (request.params["dob"]).strip()
			blood_group = (request.params["blood_group"]).strip()
			languages = [x.strip() for x in languages.split(",")]

			for l in languages:
				if l not in LANGUAGES:
					languages.remove(l)

			u = User()
			instance = u.is_valid_token(token, user_id)
			if instance:
				# Valid user
				if len(name) < 3:
					response["message"] = "Invalid name."
				elif len(dob) != 10:
					response["message"] = "Invalid date of birth."
				elif len(languages) < 3:
					response["message"] = "Invalid language."
				elif gender not in GENDER:
					response["message"] = "Invalid gender."
				elif blood_group not in BLOOD_GROUP:
					response["message"] = "Invalid blood group."
				elif not languages:
					response["message"] = "Invalid language."
				else:

					data = {
						"user_id": user_id,
						"name": name,
						"gender": gender,
						"languages": languages,
						"blood_group": blood_group,
						"dob": datetime.strptime(dob, "%d/%m/%Y").date()
					}
					p = Patient()
					is_updated = p.update_basic(data, instance)

					if is_updated:
						response["status"] = 200
						response["message"] = "Successfully updated."
					else:
						response["message"] = "Unable updated."
		except Exception as e:
			print(e)
			response["message"] = str(e)
		return response

	def update_patient_contact(self, **params):
		token = request.headers["X-Access-Key"]
		response = {"status": 400, "data": {}, "message": "Invalid access.", "access-key": token}
		try:
			user_id = (request.params["id"]).strip()
			mobile = (request.params["mobile"]).strip()
			email = (request.params["email"]).strip()
			address_line_1 = (request.params["address_line_1"]).strip()
			address_line_2 = (request.params["address_line_2"]).strip()
			address_line_3 = (request.params["address_line_3"]).strip()
			area = (request.params["area"]).strip()
			pincode = (request.params["pincode"]).strip()
			state = (request.params["state"]).strip()
			city = (request.params["city"]).strip()
			country = (request.params["country"]).strip()

			u = User()
			instance = u.is_valid_token(token, user_id)
			if instance:
				# Valid user
				if (not mobile.isdigit()) or (len(mobile) != 10):
					response["message"] = "Invalid mobile number."
				elif validate_email(email) == None:
					response["message"] = "Invalid email."
				elif len(address_line_1) < 3:
					response["message"] = "Invalid address line."
				elif len(area) < 3:
					response["message"] = "Invalid area."
				elif (len(pincode) < 5) and (not pincode.isdigit()):
					response["message"] = "Invalid pin-code."
				elif not state:
					response["message"] = "Invalid state."
				elif not city:
					response["message"] = "Invalid city."
				elif not country:
					response["message"] = "Invalid country."
				else:
					data = {
						"user_id": user_id,
						"mobile": mobile,
						"email": email,
						"address_line_1": address_line_1,
						"address_line_2": address_line_2,
						"address_line_3": address_line_3,
						"area": area,
						"pincode": pincode,
						"state": state,
						"city": city,
						"country": country
					}
					p = Patient()
					is_updated = p.update_contact(data, instance)

					if is_updated:
						response["status"] = 200
						response["message"] = "Successfully updated."
					else:
						response["message"] = "Unable updated."

		except Exception as e:
			print(e)
			response["message"] = str(e)
		return response

	def update_patient_document(self, **params):
		token = request.headers["X-Access-Key"]
		response = {"status": 400, "data": {}, "message": "Invalid access.", "access-key": token}
		try:
			form_data = {}
			user_id = (request.params["id"]).strip()
			doc_type = (request.params["doc_type"]).strip()

			if doc_type in PATIENT_DOCUMENTS:

				for key in request.params:
					form_data[key] = request.params[key]

				u = User()
				instance = u.is_valid_token(token, user_id)
				if instance:
					p = Patient()
					data = {
						"doc_type": doc_type,
						"details": json.dumps(form_data)
					}
					is_updated = p.update_document(data, instance)
					if is_updated:
						response["status"] = 200
						response["message"] = "Successfully updated."
					else:
						response["message"] = "Unable updated."
			else:
				response["message"] = "Invalid document type."


		except Exception as e:
			print(e)
			response["message"] = str(e)
		return response

	def patient_documents(self, **params):
		token = request.headers["X-Access-Key"]
		response = {"status": 400, "data": {}, "message": "Invalid access.", "access-key": token}
		try:
			user_id = (request.params["id"]).strip()
			u = User()
			instance = u.is_valid_token(token, user_id)
			if instance:
				p = Patient()
				response["status"] = 200
				response["message"] = "Patient info."
				response["data"] = p.documents(instance)
		except Exception as e:
			print(e)
			response["message"] = str(e)
		return response

	def patient_document(self, **params):
		token = request.headers["X-Access-Key"]
		response = {"status": 400, "data": {}, "message": "Invalid access.", "access-key": token}
		try:
			user_id = (request.params["id"]).strip()
			doc_type = (request.params["doc_type"]).strip()
			if doc_type in PATIENT_DOCUMENTS:
				u = User()
				instance = u.is_valid_token(token, user_id)
				if instance:
					p = Patient()
					response["status"] = 200
					response["message"] = "Patient info."
					response["data"] = p.document(instance, doc_type)
			else:
				response["message"] = "Invalid document type."

		except Exception as e:
			print(e)
			response["message"] = str(e)
		return response

	def rating(self, **params):
		return {"status": 200, "data": {}, "message": "Patient rating doctor"}

	def review(self, **params):
		return {"status": 200, "data": {}, "message": "Patient review doctor"}

	def paymet(self, **params):
		return {"message": "Patient payments"}

	def appointment(self, **params):
		return {"status": 200, "data": {}, "message": "appointment"}

	def appointments(self, **params):
		return {"status": 200, "data": {}, "message": "appointment"}

	def save_appointment(self, **params):
		return {"status": 200, "data": {}, "message": "appointment"}

	def profile(self, **params):
		return {"status": 200, "data": {}, "message": "Profile"}
