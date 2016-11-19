"""
	Basic exception classes for Meres server
"""


class MeresiaException(Exception):
	fields = []

	def __init__(self, message, code=500):
		super(MFException, self).__init__(message)
		self.code = code


class GeneralException(MeresiaException):
	pass


class UserException(MeresiaException):
	pass

class DataException(MeresiaException):
	def __init__(self, message, code=502):
		super(DataException, self).__init__(message, code)


class NetworkException(MeresiaException):
	pass
