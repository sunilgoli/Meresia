from libraries.db_connector import db_session
from libraries.util import object_to_dict_with_key
from libraries.util import object_to_list_of_dicts

from .models import Patient as PatModel
from .models import Address
from .models import Document
from .models import Language
from .models import Insurance

from modules.user.models import User
from datetime import datetime

class Patient(object):

	def register(self, data):
		try:
			u = User()
			print(u.is_duplicate("email", data["email"]))
			if u.is_duplicate("email", data["email"]):
				return {"status": False, "message": "Given email is already registered with us."}

			if u.is_duplicate("mobile", data["mobile"]):
				return {"status": False, "message": "Given mobile number is already registered with us."}

			u.email_id = data["email"]
			u.mobile = data["mobile"]
			u.status = True
			u.u_type = "Patient"
			u.password = data["password"]
			u.save()

			pat = PatModel()
			pat.name = data["name"]
			pat.email_id = data["email"]
			pat.mobile = data["mobile"]
			pat.created_at = datetime.now()
			pat.modified_at = datetime.now()
			pat.save()

			db_session.commit()
			return {"status": True, "message": "Registered  successfully."}
		except Exception as e:
			db_session.rollback()
			return {"status": False, "message": "Exception " + str(e)}

	def update_basic(self, data, instance):
		try:
			pat = PatModel()
			pat_ins = pat.info(instance.email_id)
			pat_ins.name = data["name"]
			pat_ins.gender = data["gender"]
			pat_ins.dob = data["dob"]
			pat_ins.blood_group = data["blood_group"]
			pat_ins.modified_at = datetime.now()
			pat_ins.save()

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

			db_session.commit()
			return True
		except Exception as e:
			print(e)
		return False

	def update_contact(self, data, instance):
		try:
			pat = PatModel()
			pat_ins = pat.info(instance.email_id)

			# Update doctor's email and mobile for login
			instance.email_id = data["email"]
			instance.mobile = data["mobile"]
			instance.save()

			# Update doctor's email and mobile
			pat_ins.email_id = data["email"]
			pat_ins.mobile = data["mobile"]
			pat_ins.save()

			# Update address
			addr = Address()
			addr_inst = addr.instance(pat_ins.id)
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
				addr.patient_id = pat_ins.id
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
			print(e)
		return False

	def update_document(self, data, instance):
		try:
			pat = PatModel()
			pat_ins = pat.info(instance.email_id)

			doc = Document()
			doc_inst = doc.instance(pat_ins.id, data["doc_type"])
			if doc_ins:
				# Update document info
				doc_ins.details = data["details"]
				doc_ins.modified_at = datetime.now()
				doc_ins.save()
			else:
				# Save document info
				doc.patient_id = pat_ins.id
				doc.doc_type = data["doc_type"]
				doc.details = data["details"]
				doc.created_at = datetime.now()
				doc.modified_at = datetime.now()
				doc.save()

			db_session.commit()
			return True
		except Exception as e:
			print(e)
		return False

	def documents(self, instance):
		try:
			pat = PatModel()
			pat_ins = pat.info(instance.email_id)

			doc = Document()
			return object_to_list_of_dicts(["doc_type", "details"], doc.list(pat_ins.id))
		except Exception as e:
			print(e)
		return []

	def document(self, instance, doc_type):
		try:
			pat = PatModel()
			pat_ins = pat.info(instance.email_id)

			doc = Document()
			return object_to_list_of_dicts(["doc_type", "details"], doc.list(pat_ins.id))
		except Exception as e:
			print(e)
		return []

	def insurance(self, instance):
		try:
			pat = PatModel()
			pat_ins = pat.info(instance.email_id)
			pass
		except Exception as e:
			print(e)
		return []
