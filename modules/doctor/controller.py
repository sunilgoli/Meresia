from libraries.db_connector import db_session
from libraries.util import object_to_dict_with_key
from libraries.util import object_to_list_of_dicts

from .models import Doctor as DocModel
from .models import Specialty
from .models import Language
from .models import Address
from .models import Consultation
from .models import Clinic

from modules.user.models import User
from datetime import datetime


class Doctor(object):

	def register(self, data):
		try:
			u = User()
			doc = DocModel()
			if u.is_duplicate("email", data["email"]):
				return {"status": False, "message": "Given email is already registered with us."}

			if u.is_duplicate("mobile", data["mobile"]):
				return {"status": False, "message": "Given mobile number is already registered with us."}

			if doc.is_duplicate("registration_number", data["registration_number"]):
				return {"status": False, "message": "Given doctor registration number is already registered."}

			u.email_id = data["email"]
			u.mobile = data["mobile"]
			u.status = False
			u.u_type = "Doctor"
			u.password = data["password"]
			u.save()

			doc.name = data["name"]
			doc.email_id = data["email"]
			doc.mobile = data["mobile"]
			doc.registration_number = data["registration_number"]
			doc.degree = data["degree"]
			doc.status = True
			doc.created_at = datetime.now()
			doc.modified_at = datetime.now()
			doc.save()
			db_session.commit()

			spec = Specialty()
			spec.doctor_id = doc.id
			spec.specialty = data["specialization"]
			spec.created_at = datetime.now()
			spec.modified_at = datetime.now()
			spec.save()
			db_session.commit()
			return {"status": True, "message": "Registered  successfully."}
		except Exception as e:
			db_session.rollback()
			return {"status": False, "message": "Exception " + str(e)}

	def update_basic(self, data, instance):
		try:
			# Doctor update
			doc = DocModel()
			doc_ins = doc.info(instance.email_id)
			doc_ins.name = data["name"]
			doc_ins.degree = data["degree"]
			doc_ins.gender = data["gender"]
			doc_ins.experience = data["experience"]
			doc_ins.dob = data["dob"]
			doc_ins.modified_at = datetime.now()
			doc_ins.save()

			# Language update
			lan = Language()
			languages = object_to_dict_with_key("lan_type", lan.list(doc_ins.id))

			for language in data["languages"]:
				if language in languages:
					del languages[language]
				else:
					new_lan = Language()
					new_lan.doctor_id = doc_ins.id
					new_lan.lan_type = language
					new_lan.created_at = datetime.now()
					new_lan.modified_at = datetime.now()
					new_lan.save()

			# Deleting languages which are deselected by doctor
			for key,obj in languages.items():
				lan.delete(obj)

			# Specialty update
			spec = Specialty()
			specialties = object_to_dict_with_key("specialty", spec.list(doc_ins.id))
			for specialty in data["specialties"]:
				if specialty in specialties:
					del specialties[specialty]
				else:
					new_spec = Specialty()
					new_spec.doctor_id = doc_ins.id
					new_spec.specialty = specialty
					new_spec.created_at = datetime.now()
					new_spec.modified_at = datetime.now()
					new_spec.save()

			# Deleting specialties which are deselected by doctor
			for key,obj in specialties.items():
				spec.delete(obj)
			db_session.commit()
			return True
		except Exception as e:
			print("str " + str(e))
			db_session.rollback()
			return False

	def update_contact(self, data, instance):
		try:
			# Doctor instance before update
			doc = DocModel()
			doc_ins = doc.info(instance.email_id)

			# Update doctor's email and mobile for login
			instance.email_id = data["email"]
			instance.mobile = data["mobile"]
			instance.save()

			# Update doctor's email and mobile
			doc_ins.email_id = data["email"]
			doc_ins.mobile = data["mobile"]
			doc_ins.save()

			# Update address
			addr = Address()
			addr_inst = addr.instance(doc_ins.id)
			if addr_inst:
				# Update
				addr_inst.address_line_1 = data["address_line_1"]
				addr_inst.address_line_2 = data["address_line_2"]
				addr_inst.address_line_3 = data["address_line_3"]
				addr_inst.area = data["area"]
				addr_inst.city = data["city"]
				addr_inst.state = data["state"]
				addr_inst.country = data["country"]
				addr_inst.pincode = data["pincode"]
				addr_inst.modified_at = datetime.now()
				addr_inst.save()
			else:
				# Add
				addr.doctor_id = doc_ins.id
				addr.address_line_1 = data["address_line_1"]
				addr.address_line_2 = data["address_line_2"]
				addr.address_line_3 = data["address_line_3"]
				addr.area = data["area"]
				addr.city = data["city"]
				addr.state = data["state"]
				addr.country = data["country"]
				addr.pincode = data["pincode"]
				addr.created_at = datetime.now()
				addr.modified_at = datetime.now()
				addr.save()

			db_session.commit()
			return True
		except Exception as e:
			db_session.rollback()
			print(e)
			return False

	def update_consultation(self, data, instance):
		try:
			doc = DocModel()
			doc_ins = doc.info(instance.email_id)

			cons = Consultation()
			consultations = object_to_dict_with_key("mode", cons.list(doc_ins.id))

			for consultation in data:
				if consultation in consultations:
					obj = consultations[consultation]
					obj.price = data[consultation]
					obj.modified_at = datetime.now()
					obj.save()
				else:
					cons_inst = Consultation()
					cons_inst.doctor_id = doc_ins.id
					cons_inst.mode = consultation
					cons_inst.price = data[consultation]
					cons_inst.created_at = datetime.now()
					cons_inst.modified_at = datetime.now()
					cons_inst.save()

			db_session.commit()
			return True
		except Exception as e:
			db_session.rollback()
			print(e)
			return False

	def update_clinic(self, data, instance):
		try:
			doc = DocModel()
			doc_ins = doc.info(instance.email_id)

			cli = Clinic()
			if data["clinic_id"] != 0:
				cli_upd = cli.instance(doc_ins.id, data["clinic_id"])
				if cli_upd:
					cli_upd.hospital = data["hospital"]
					cli_upd.city = data["city"]
					cli_upd.state = data["state"]
					cli_upd.pincode = data["pincode"]
					cli_upd.start_date = data["start_date"]
					cli_upd.end_date = data["end_date"]
					cli_upd.modified_at = datetime.now()
					cli_upd.save()
				else:
					print("Invalid clinic for the doctor")
			else:
				cli.doctor_id = doc_ins.id
				cli.hospital = data["hospital"]
				cli.city = data["city"]
				cli.state = data["state"]
				cli.pincode = data["pincode"]
				cli.start_date = data["start_date"]
				cli.end_date = data["end_date"]
				cli.status = True
				cli.created_at = datetime.now()
				cli.modified_at = datetime.now()
				cli.save()

			db_session.commit()
			return True
		except Exception as e:
			db_session.rollback()
			print(e)
		return False

	def clinics(self, instance):
		try:
			doc = DocModel()
			doc_ins = doc.info(instance.email_id)
			cli = Clinic()
			return object_to_list_of_dicts(["id", "hospital", "city", "state", "pincode", "start_date", "end_date"], cli.list(doc_ins.id))
		except Exception as e:
			print(e)
		return {}

	def pricing(self, instance):
		try:
			doc = DocModel()
			doc_ins = doc.info(instance.email_id)
			cons = Consultation()
			return object_to_list_of_dicts(["mode", "price"], cons.list(doc_ins.id))
		except Exception as e:
			print(e)
		return {}
