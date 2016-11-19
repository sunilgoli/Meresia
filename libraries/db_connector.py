from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.constants import db_user, db_password, db_name, db_host, db_autocommit, db_autoflush

"""
	DB Connector
"""
db_engine = create_engine("postgresql://" + db_user + ":" + db_password + "@" + db_host + "/" + db_name, convert_unicode=True)

""" Create DB session object """
db_session = scoped_session(sessionmaker(autocommit=db_autocommit, autoflush=db_autoflush, bind=db_engine))

Base = declarative_base(bind=db_engine)
Base.query = db_session.query_property()


# DB creation
def init_db():

	# Doctor modules
	from modules.doctor.models import Doctor
	from modules.doctor.models import Specialty
	from modules.doctor.models import Language
	from modules.doctor.models import Address
	from modules.doctor.models import Consultation
	from modules.doctor.models import Clinic

	# Patient modules
	from modules.patient.models import Patient
	from modules.patient.models import Address
	from modules.patient.models import Document
	from modules.patient.models import Language
	# from modules.patient.models import Insurance

	# Patient modules
	from modules.user.models import User

	# Patient modules
	from modules.appointment.models import Appointment

	# payment modules
	# from modules.payment.models import Payment

	# review modules
	# from modules.review.models import Review

	# rating modules
	# from modules.rating.models import Rating


	""" Create all tables if not existing """
	Base.metadata.create_all(bind=db_engine)