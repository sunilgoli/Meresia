import cherrypy
import config.config as settings
from libraries.util import JSONEncoder
from routes import Mapper
import simplejson as json
import libraries.exceptions as ex

import logging


class Server(object):
	"""
	The Server class uses _cp_dispatch to catch all http requests.
	and process them based on the route map
	"""

	def __init__(self):
		self._map = self._prepare_map()

	@cherrypy.expose
	def default(self, **params):
		return "hello world"

	def _cp_dispatch(self, vpath):
		"""Handle all requests."""
		if vpath[0] == "dummy.html":  # ignore, cherrypy"s internal call
			return vpath

		# match
		match = self._map.match("/" + "/".join(vpath), environ={"REQUEST_METHOD": cherrypy.request.method})

		if match:
			vpath[:] = []
			route_name = match["route_name"]
			del match["route_name"]
			return Dispatcher(route_name, match)

		# no mapped routes
		return vpath

	def _prepare_map(self):
		"""Setup the route map with the Routes lib."""
		m = Mapper()

		# connect our routes to the mapper
		for name, route in settings.routes.items():
			m.connect(name, route["route"],
						route_name=name,
						conditions={"method": route["methods"]
									\
									if "methods" in route else []})
		return m


class Dispatcher(object):
	"""Takes a route defined in settings and dispatches its controller."""

	def __init__(self, route_name, route_params):
		self.route = settings.routes[route_name]
		self.route_params = route_params

	@cherrypy.expose
	def index(self, **params):
		"""Catch-all controller for handling and routing all incoming requests."""
		# merge params from the server (cherrypy) + params from Routes
		params = dict(params.items() + self.route_params.items())

		# user_id is required by every single request
		# params["user_id"] = cherrypy.request.params.get("user_id").upper()

		# instantiate the appropriate controller
		target = self.route["controller"]

		# the class
		target_class = target.im_class

		# insantiate the class
		target_instance = target_class()

		target_method = target.__get__(target_instance, target_class)

		# run the controller, get the response
		try:
			resp = target_method(**params)
			return self._respond(resp, resp["status"])
		except Exception as e:
			if settings.environment != "production":
				raise

			if isinstance(e, ex.MFException):  # there"s a MF error
				return self._error(e)
			else:
				return self._error(ex.GeneralException("An internal server error occurred", code=500))

	def _error(self, e):
		"""Error response."""
		if settings.environment != "production":
			raise Exception(e.message)

		data = {"status": "error",
				"message": e.message,
				"error_type": e.__class__.__name__}

		# additional data that has to go with the error message
		for f in e.fields:
			data[f] = getattr(e, f)

		cherrypy.response.status = e.code
		return self._respond(data, e.code)

	def _respond(self, response, e_code):
		"""Send a JSON encoded response to the world."""
		# Response status code
		cherrypy.response.status = e_code
		# Set access token in the response header
		cherrypy.response.headers["ACCESS-KEY"] = response["access-key"]
		# Once access token is set remove it from response
		del response["access-key"]

		if settings.environment != "production":
			return json.dumps(response, indent=4, cls=JSONEncoder)
		else:
			return json.dumps(response, cls=JSONEncoder)


def cors():
	"""Cor handler."""
	cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"


def error_page_404(status, message, traceback, version):
	"""Error page handler function."""
	response = cherrypy.response
	response.headers["Content-Type"] = "application/json"
	return json.dumps({"status": 400, "message": "Bad request"})


def start():
	"""Start server."""
	cherrypy.tools.CORS = cherrypy.Tool('before_handler', cors)
	config = {
		"/": {
			#  "error_page.default": View.error_page,
			"tools.trailing_slash.on": False,
			"tools.CORS.on": True,
			"log.error_file": settings.server["error_logs"]
		}
	}

	cherrypy.config.update({
		#  "environment": "production",
		"server.socket_host": settings.server["host"],
		"server.socket_port": settings.server["port"],
		"server.thread_pool": settings.server["threads"],
		'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
		"tools.CORS.on": True,
		"autoreload.on": False,
		"log.screen": False,
		#  "tools.encode.on": True,
		"tools.encode.encoding": "utf-8",
		"tools.response_headers.on": True,
		"request.show_tracebacks": False,
		"error_page.404": error_page_404,
		"tools.response_headers.headers": [("Content-Type", "application/json")],
	})
	cherrypy.response.timeout = settings.server["timeout"]
	cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
	cherrypy.response.headers["Allow"] = "GET, POST, PUT, DELETE, OPTIONS"

	"""
		Log all exception.
	"""
	#  logging types : DEBUG, INFO, Warning, error, critical, log, exception
	logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s',
						datefmt='%a, %d %b %Y %H:%M:%S',
						level=logging.DEBUG,
						filename=settings.server["exception_logs"])

	app = cherrypy.tree.mount(Server(), "/", config=config)
	cherrypy.quickstart(app)

if __name__ == "__main__":
	start()
