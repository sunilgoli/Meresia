from libraries.db_connector import db_session, Base, db_engine
from libraries.db_util import literalquery
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import Enum, Numeric
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime


class User(Base):
	__tablename__ = "addict"

	id = Column(Integer, primary_key=True, index=True)
	email_id = Column(String(250), index=True, unique=True)
	mobile = Column(Numeric(15), index=True, unique=True)
	password = Column(String(260), index=True)
	u_type = Column(Enum("Doctor", "Patient", "Admin", "Supervisor", "Blocked", "Suspended", "Pending", name="user_type"), index=True)
	tocken = Column(String(260), index=True, nullable=True)
	status = Column(Boolean, index=True)
	last_login = Column(DateTime)

	"""docstring for Model"""
	def __init__(self):
		pass

	def save(self):
		try:
			db_session.add(self)
		except Exception as e:
			print(e)
			raise False

	def update(self, data):
		try:
			instance = db_session.query(User)
			instance = instance.filter(User.id == self.id)
			instance.update(data)
			db_session.commit()
		except Exception as e:
			print(str(e))
			raise False

	def has_valid_credentials(self, data):
		try:
			instance = db_session.query(User)
			# instance = instance.filter(or_(User.email_id == data["username"], User.mobile == data["username"]))
			if data["username"].isdigit():
				instance = instance.filter(User.mobile == data["username"])
			else:
				instance = instance.filter(User.email_id == data["username"])
			instance = instance.filter(User.password == data["password"])
			instance = instance.filter(User.status == True)
			return instance.one()
		except Exception as e:
			print(str(e))
			return False

	def is_duplicate(self, attribute, search_for):
		try:
			instance = db_session.query(User)
			if attribute == "email":
				instance = instance.filter(User.email_id == search_for)
			elif (attribute == "mobile") and (search_for.isdigit()):
				instance = instance.filter(User.mobile == search_for)
			else:
				return True
			return instance.one()
		except NoResultFound as e:
			return False
		except Exception as e:
			print(str(e))
			return True

	def is_valid_token(self, token, user_id):
		try:
			instance = db_session.query(User)
			instance = instance.filter(User.tocken == token)
			instance = instance.filter(User.id == int(user_id))

			# To print raw query
			# print(literalquery(instance))
			return instance.one()
		except Exception as e:
			print(e)
			return False
