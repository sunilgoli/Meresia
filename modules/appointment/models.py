from libraries.db_connector import db_session, Base

from sqlalchemy import Column, Integer, String, Boolean, Time
from sqlalchemy import Enum, func, DateTime, Date, Numeric, ForeignKey
from sqlalchemy.sql.expression import literal_column, case
from sqlalchemy.sql.functions import concat
from sqlalchemy.orm import relationship

from datetime import datetime

class Appointment(Base):
	__tablename__ = "consultation"

	id = Column(Integer, primary_key=True, index=True)
	doctor_id = Column(Integer, ForeignKey("doctor.id"), index=True, nullable=False)
	patient_id = Column(Integer, ForeignKey("patient.id"), index=True, nullable=True)
	refer_doctor_id = Column(Integer, ForeignKey("doctor.id"), index=True, nullable=True)
	for_date = Column(Date, index=True)
	slot_start = Column(Time, index=True) #datetime.time
	slot_end = Column(Time, index=True) #datetime.time
	mode = Column(Enum("Call", "Video", "Mail", "Chat", "Blocked", name="appointment_mode"), index=True)
	prescription = Column(String(5000))
	tests = Column(String(5000))
	remarks = Column(String(5000))
	further_consultation = Column(Boolean)
	status = Column(Enum("Start", "Processing", "Scheduled", "Rescheduled", "Canceled", "Completed", "Blocked", name="appointment_status"), index=True)
	created_at = Column(DateTime)
	modified_at = Column(DateTime)

	"""docstring for Docpat"""
	def __init__(self):
		pass
