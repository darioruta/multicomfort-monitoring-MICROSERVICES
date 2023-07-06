class de ():
	
	'''

	Class dedicated to 'store' globals definitions of variables

	'''

	def __init__(self):

		self.localhost = "localhost"
		self.port = "port"

		self.history = "history"
		self.timestamp = "timestamp"
		self.timestamps = "timestamps"
		self.values = "values"
		self.value = "value"
		self.t = "t"
		self.d = "d"
		self.h = "h"

		self.sensorID = "sensorID"
		self.ALLsensors = [0]
		self.limit_DEFAULT = 1 # prendo l'ultima presente
		self.limit_MAX = 50 # non si possono prendere piú di 50 misurazioni

		# utilizzata per semplificare il numero di linee di codice
		self.type_measurements = [self.t, self.h, self.d]

		self.KEY_PAIR = 0
		self.VALUE_PAIR = 1

		self.cloud_PATH_DEFAULT = "./data/stored_test/history.json"
		self.cat_loc_1_PATH = "./data/stored_test/locality_catalog.json"
		self.cat_cannons_1_PATH = "./data/stored_test/cannons_catalog.json"
		self.cat_sensors_1_PATH = "./data/stored_test/sensors_catalog.json"

		self.path_end_cannons = "/cannons_catalog.json"
		self.path_end_sensors = "/sensors_catalog.json"
		self.path_end_locality = "/locality_catalog.json"
		self.path_end_history = "/history.json"
