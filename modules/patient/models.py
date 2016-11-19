from libraries.db_connector import db_session, Base, db_engine

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import Enum, func, DateTime, Date, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.sql.expression import literal_column, case
from sqlalchemy.sql.functions import concat
from sqlalchemy.orm import relationship

from datetime import datetime


class Patient(Base):
	__tablename__ = "patient"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(250), index=True)
	email_id = Column(String(250), index=True, unique=True)
	mobile = Column(Numeric(15), index=True, unique=True)
	gender = Column(Enum("M", "F", "T", name="gender"), index=True)
	dob = Column(Date, index=True)
	blood_group = Column(Enum("O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+", name="blood_group"), index=True)
	pic_path = Column(String(250))
	status = Column(Boolean, index=True)
	created_at = Column(DateTime)
	modified_at = Column(DateTime)

	"""docstring for Patient"""
	def __init__(self):
		pass

	def save(self):
		try:
			db_session.add(self)
		except Exception as e:
			print(e)
			return False

	def info(self, email):
		try:
			instance = db_session.query(Patient)
			instance = instance.filter(Patient.email_id == email)
			return instance.one()
		except Exception as e:
			print(str(e))
			return False


class Address(Base):
	__tablename__ = "patient_address"

	id = Column(Integer, primary_key=True, index=True)
	patient_id = Column(Integer, ForeignKey("patient.id"), index=True, nullable=False)
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
			return False

	def instance(self, patient_id):
		try:
			instance = db_session.query(Address)
			instance = instance.filter(Address.patient_id == patient_id)
			return instance.one()
		except Exception as e:
			print(str(e))
			return False

	def info(self, patient_id):
		try:
			instance = db_session.query(Address)
			instance = instance.filter(Address.patient_id == patient_id)
			return instance.one()
		except Exception as e:
			print(str(e))
			return {"address_line_1": "", "address_line_2": "", "address_line_3": "", "area": "", "city": "", "state": "", "country": "", "pincode": ""}


class Document(Base):
	__tablename__ = "document"

	id = Column(Integer, primary_key=True, index=True)
	patient_id = Column(Integer, ForeignKey("patient.id"), index=True, nullable=False)
	doc_type = Column(Enum("Basic Details",
		"Medications",
		"Immunizations",
		"Latest Consultations",
		"Allergies",
		"Family and Social History",
		"Surgeries/Procedures",
		"Addictions",
		"Hospitalization",
		"Contact Details",
		"Lab Reports",
		"Medical Documents", name="document_type"), index=True)
	details = Column(JSONB)
	created_at = Column(DateTime)
	modified_at = Column(DateTime)

	"""docstring for Document"""
	def __init__(self):
		pass

	def save(self):
		try:
			db_session.add(self)
		except:
			return False

	def instance(self, patient_id, doc_type):
		try:
			instance = db_session.query(Document)
			instance = instance.filter(Document.patient_id == patient_id)
			instance = instance.filter(Document.doc_type == doc_type)
			return instance.one()
		except Exception as e:
			print(str(e))
			return False

	def list(self, patient_id):
		try:
			instance = db_session.query(Document)
			instance = instance.filter(Document.patient_id == patient_id)
			return instance.all()
		except Exception as e:
			print(str(e))
			return {}

	def info(self, patient_id, doc_type):
		try:
			instance = db_session.query(Document)
			instance = instance.filter(Document.patient_id == patient_id)
			instance = instance.filter(Document.doc_type == doc_type)
			return instance.one()
		except Exception as e:
			print(str(e))
			return False


class Language(Base):
	__tablename__ = "patient_language"

	id = Column(Integer, primary_key=True, index=True)
	patient_id = Column(Integer, ForeignKey("patient.id"), index=True, nullable=False)
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
		# Save or update instance
		try:
			db_session.add(self)
		except:
			return False

	def list(self, patient_id):
		# list of all the languages which patient knows
		try:
			instance = db_session.query(Language)
			instance = instance.filter(Language.patient_id == patient_id)
			return instance.all()
		except Exception as e:
			print(str(e))
			return {}

	def delete(self, instance):
		# Deleting an instance or a language
		try:
			return db_session.query(Language).filter(Language.id == instance.id).delete()
		except Exception as e:
			print(e)
			return False


class Insurance(Base):
	__tablename__ = "insurance"

	id = Column(Integer, primary_key=True, index=True)
	patient_id = Column(Integer, ForeignKey("patient.id"), index=True, nullable=False)


	"""docstring for Insurance"""
	def __init__(self):
		pass

	def save(self):
		try:
			db_session.add(self)
		except:
			return False

	def list(self, patient_id):
		try:
			pass
		except Exception as e:
			print(str(e))
			return {}
