from libraries.db_connector import db_engine
from libraries.util import generate_token, object_to_list_of_dicts
from datetime import datetime

from .models import User as UserModel
from modules.patient.models import Patient, Address as PatAddr
from modules.patient.models import Language as PatLan
from modules.doctor.models import Doctor, Specialty, Language as DocLan
from modules.doctor.models import Clinic, Consultation, Address as DocAddr


class User(object):

	"""docstring for User"""
	def __init__(self):
		pass

	def register(self, data):
		pass

	def has_valid_credentials(self, credentials):
		# Verify user credentials
		response = {"access_key": None, "data": {}}
		try:
			u = UserModel()
			instance = u.has_valid_credentials(credentials)
			if instance:
				access_key = generate_token(instance.id)
				# Set access key and return access key
				info = {}

				if instance.u_type in ["Doctor", "Patient"]:
					if instance.u_type == "Doctor":
						d = Doctor()
						info = self.__doctor(instance.id, d.info(instance.email_id))
					else:
						p = Patient()
						info = self.__patient(instance.id, p.info(instance.email_id))

				instance.update({"tocken": access_key, "last_login": datetime.now()})
				response["access_key"] = access_key
				response["data"] = info

		except Exception as e:
			print(str(e))
		return response

	def info(self, instance):
		info = {}
		try:
			if instance.u_type in ["Doctor", "Patient"]:
				if instance.u_type == "Doctor":
					d = Doctor()
					info = self.__doctor(instance.id, d.info(instance.email_id))
				else:
					p = Patient()
					info = self.__patient(instance.id, p.info(instance.email_id))
		except Exception as e:
			print(e)
		return info

	def __doctor(self, user_id, instance):
		info = {}
		try:
			s = Specialty()
			l = DocLan()
			a = DocAddr()
			c = Consultation()
			h = Clinic()
			info["id"] = user_id
			info["name"] = instance.name
			info["user_type"] = "Doctor"
			info["mobile"] = instance.mobile
			info["email"] = instance.email_id
			info["gender"] = instance.gender
			info["degree"] = instance.degree
			info["experience"] = instance.experience
			info["registration_number"] = instance.registration_number
			info["dob"] = (instance.dob).strftime('%d/%m/%Y')
			info["pic_path"] = instance.pic_path
			info["registered_on"] = instance.created_at
			info["last_updated"] = instance.modified_at
			info["specialties"] = object_to_list_of_dicts(["specialty"], s.list(instance.id))

			info["languages"] = object_to_list_of_dicts(["lan_type"], l.list(instance.id))

			addr = a.info(instance.id)
			info["address"] = {
				"address_line_1": addr.address_line_1,
				"address_line_2": addr.address_line_2,
				"address_line_3": addr.address_line_3,
				"area": addr.area,
				"pincode": addr.pincode,
				"state": addr.state,
				"city": addr.city,
				"country": addr.country
			}

			info["consultation"] = object_to_list_of_dicts(["mode", "price"], c.list(instance.id))

			info["hospitals"] = object_to_list_of_dicts(["hospital", "city", "state", "pincode", "start_date", "end_date"], h.list(instance.id))
		except Exception as e:
			print(e)
		return info

	def __patient(self, user_id, instance):
		info = {}
		try:
			a = PatAddr()
			l = PatLan()
			info["id"] = user_id
			info["name"] = instance.name
			info["user_type"] = "Patient"
			info["mobile"] = instance.mobile
			info["email"] = instance.email_id
			info["gender"] = instance.gender
			info["dob"] = instance.dob
			info["blood_group"] = instance.blood_group
			info["pic_path"] = instance.pic_path
			info["registered_on"] = instance.created_at
			info["last_updated"] = instance.modified_at
			info["address"] = a.info(instance.id)
			info["languages"] = object_to_list_of_dicts(["lan_type"], l.list(instance.id))
		except Exception as e:
			print(e)
		return info

	def is_valid_token(self, token, user_id):
		u = UserModel()
		instance = u.is_valid_token(token, user_id)
		return instance
