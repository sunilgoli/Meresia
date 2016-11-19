from libraries.db_connector import db_session, Base, db_engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy import Enum, func, DateTime, Date, Numeric
from sqlalchemy.sql.expression import literal_column, case
from sqlalchemy.sql.functions import concat
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime


class Doctor(Base):
	__tablename__ = "doctor"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(250), index=True)
	email_id = Column(String(250), index=True, unique=True)
	mobile = Column(Numeric(15), index=True, unique=True)
	gender = Column(Enum("M", "F", "T", name="gender"), index=True)
	degree = Column(String(250))
	experience = Column(Numeric(2))
	registration_number = Column(String(20), index=True, unique=True)
	dob = Column(Date, index=True)
	pic_path = Column(String(250))
	status = Column(Boolean, index=True)
	created_at = Column(DateTime)
	modified_at = Column(DateTime)


	"""docstring for Model"""
	def __init__(self):
		pass

	def save(self):
		try:
			db_session.add(self)
		except:
			raise False

	def is_duplicate(self, attribute, search_for):
		try:
			instance = db_session.query(Doctor)
			if attribute == "registration_number":
				instance = instance.filter(Doctor.registration_number == search_for)
			else:
				return True
			return instance.one()
		except NoResultFound as e:
			return False
		except Exception as e:
			print(e)
			return True

	def info(self, email):
		try:
			instance = db_session.query(Doctor)
			instance = instance.filter(Doctor.email_id == email)
			return instance.one()
		except Exception as e:
			print(str(e))
			return {}


class Specialty(Base):
	__tablename__ = "doc_specialty"

	id = Column(Integer, primary_key=True, index=True)
	doctor_id = Column(Integer, ForeignKey("doctor.id"), index=True, nullable=False)
	specialty = Column(Enum("Adolescent medicine",
		"Allergy and immunology",
		"Allergist or Immunologist",
		"Anesthesiologist",
		"Cardiologist",
		"Cardiothoracic surgery",
		"Clinical neurophysiology",
		"Dermatologist",
		"Dietetics",
		"Endocrinology",
		"Gastroenterologist",
		"Geriatrics",
		"Gynecologist",
		"Hematologist",
		"Internal Medicine Physician",
		"Nephrologist",
		"Neurologist",
		"Neurosurgeon",
		"Obstetrician",
		"Oncologist",
		"Nurse-Midwifery",
		"Occupational Medicine Physician",
		"Ophthalmologist",
		"Oral and Maxillofacial Surgeon",
		"Orthopaedic",
		"Otolaryngologist",
		"Paediatric cardiology",
		"Pathologist",
		"Pediatrician",
		"Plastic",
		"Podiatrist",
		"Proctologist",
		"Psychiatrist",
		"Pulmonary Medicine Physician",
		"Radiation Onconlogist",
		"Diagnostic Radiologist",
		"Radiotherapist",
		"Rheumatologist",
		"Urologist",
		"Venereology", name="specility_type"), index=True)
	created_at = Column(DateTime)
	modified_at = Column(DateTime)


	"""docstring for DoctorSpecialty"""
	def __init__(self):
		pass

	def save(self):
		try:
			db_session.add(self)
		except:
			raise False

	def list(self, doctor_id):
		try:
			instance = db_session.query(Specialty)
			instance = instance.filter(Specialty.doctor_id == doctor_id)
			return instance.all()
		except Exception as e:
			print(str(e))
			return {}

	def delete(self, instance):
		try:
			return db_session.query(Specialty).filter(Specialty.id == instance.id).delete()
		except Exception as e:
			print(e)
			return False


class Language(Base):
	__tablename__ = "doc_language"

	id = Column(Integer, primary_key=True, index=True)
	doctor_id = Column(Integer, ForeignKey("doctor.id"), index=True, nullable=False)
	lan_type = Column(Enum("Assamese",
		"Bengali",
		"Bodo",
		"Dogri",
		"English",
		"Gujarati",
		"Hindi",
		"Kannada",
		"Kashmiri",
		"Konkani",
		"Manipuri",
		"Maithili",
		"Malayalam",
		"Marathi",
		"Nepali",
		"Odia",
		"Punjabi",
		"Sindhi",
		"Tamil",
		"Telugu",
		"Tulu",
		"Urdu", name="language_type"), index=True)
	created_at = Column(DateTime)
	modified_at = Column(DateTime)


	"""docstring for DoctorSpecialty"""
	def __init__(self):
		pass

	def save(self):
		try:
			db_session.add(self)
		except:
			raise False

	def list(self, doctor_id):
		try:
			instance = db_session.query(Language)
			instance = instance.filter(Language.doctor_id == doctor_id)
			return instance.all()
		except Exception as e:
			print(str(e))
			return {}

	def delete(self, instance):
		try:
			return db_session.query(Language).filter(Language.id == instance.id).delete()
		except Exception as e:
			print(e)
			return False


class Address(Base):
	__tablename__ = "doc_address"

	id = Column(Integer, primary_key=True, index=True)
	doctor_id = Column(Integer, ForeignKey("doctor.id"), index=True, nullable=False)
	address_line_1 = Column(String(255))
	address_line_2 = Column(String(255))
	address_line_3 = Column(String(255))
	area = Column(String(155))
	city = Column(String(155))
	state = Column(String(155))
	country = Column(String(155))
	pincode = Column(Numeric(10))
	created_at = Column(DateTime)
	modified_at = Column(DateTime)


	"""docstring for DoctorAddress"""
	def __init__(self):
		pass

	def save(self):
		try:
			db_session.add(self)
		except:
			raise False

	def instance(self, doctor_id):
		try:
			instance = db_session.query(Address)
			instance = instance.filter(Address.doctor_id == doctor_id)
			return instance.one()
		except Exception as e:
			print(str(e))
			return False

	def info(self, doctor_id):
		try:
			instance = db_session.query(Address)
			instance = instance.filter(Address.doctor_id == doctor_id)
			return instance.one()
		except Exception as e:
			print(str(e))
			return {"address_line_1": "", "address_line_2": "", "address_line_3": "", "area": "", "city": "", "state": "", "country": "", "pincode": ""}


class Consultation(Base):
	__tablename__ = "doc_consultation"

	id = Column(Integer, primary_key=True, index=True)
	doctor_id = Column(Integer, ForeignKey("doctor.id"), index=True, nullable=False)
	mode = Column(Enum("Call", "Video", "Mail", "Chat", "Appointment", name="mode"), index=True)
	price = Column(Numeric(6))
	created_at = Column(DateTime)
	modified_at = Column(DateTime)


	"""docstring for DoctorConsultation"""
	def __init__(self):
		pass

	def save(self):
		try:
			db_session.add(self)
		except:
			raise False

	def list(self, doctor_id):
		try:
			instance = db_session.query(Consultation)
			instance = instance.filter(Consultation.doctor_id == doctor_id)
			return instance.all()
		except Exception as e:
			print(str(e))
			return {}


class Clinic(Base):
	__tablename__ = "doc_clinic"

	id = Column(Integer, primary_key=True, index=True)
	doctor_id = Column(Integer, ForeignKey("doctor.id"), index=True, nullable=False)
	hospital = Column(String(255))
	city = Column(String(155))
	state = Column(String(155))
	pincode = Column(Numeric(10))
	start_date = Column(Date, index=True)
	end_date = Column(Date, index=True)
	status = Column(Boolean, index=True)
	created_at = Column(DateTime)
	modified_at = Column(DateTime)


	"""docstring for DoctorWork"""
	def __init__(self):
		pass

	def save(self):
		try:
			db_session.add(self)
		except:
			raise False

	def instance(self, doctor_id, clinic_id):
		try:
			instance = db_session.query(Clinic)
			instance = instance.filter(Clinic.id == clinic_id)
			instance = instance.filter(Clinic.doctor_id == doctor_id)
			return instance.one()
		except Exception as e:
			print(e)
		return False

	def list(self, doctor_id):
		try:
			instance = db_session.query(Clinic)
			instance = instance.filter(Clinic.doctor_id == doctor_id)
			return instance.all()
		except Exception as e:
			print(str(e))
			return {}
