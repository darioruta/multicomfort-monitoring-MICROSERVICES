


class de ():

	'''

	Class dedicated to 'store' globals definitions of variables

	'''

	def __init__(self):
	

		self.localhost = "localhost"
		self.port = "port"

		self.influxDB_token = "influxDB_token"
		self.influxDB_url = "influxDB_url"
		self.influxDB_org = "influxDB_org"
		

		self.history = "history"
		self.timestamp = "timestamp"
		self.timestamps = "timestamps"
		self.values = "values"
		self.value = "value"
		self.t = "t"
		self.d = "d"
		self.h = "h"

		self.ALLkits = [0]
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
		self.path_end_dev_cat = "/dev_cat.json"

		self.sensors_catalog_ID = "sensors_catalogID"
		self.kits = "kits"
		self.kitID = "kitID"
		self.data = "data"
		self.temperature = "temperature"
		self.humidity = "humidity"
		self.deepsensor = "deepsensor"
		
		self.info_client= "info_client"
		self.kit_name = "kit_name"
		self.sensor_model = "sensor_model"
		self.date_assembly = "date_assembly"
		


		self.localityName = "localityName"
		self.path = "path"
		self.num_slopes = "num_slopes"
		
		self.localities = "localities"
		self.localityID = "localityID"
		self.info = "info"
		self.mslm = "mslm"
		
		self.plessi = "plessi"
		self.plessoID = "plessoID"
		self.aule = "aule"
		self.aulaID = "aulaID"
		
		self.timestamp = "timestamp"

   

		self.broker_address = "broker_address"
		self.broker_port = "broker_port"
		self.topic_subscribe = "topic_subscribe"
		
		
		self.cannons = "cannons"

		self.cannons_catalog_ID = "cannons_catalog_ID"
		self.cannonID = "cannonID"
		self.type = "type"
		self.mode = "mode"
		self.state = "state"
		self.info = "info"
		self.prog_on = "prog-on"
		self.prog_off = "prog-off"
		self.auto_threshold = "auto-threshold"
		self.info_client = "info_client"
		self.cannon_name = "cannon_name"
		self.cannon_model = "cannon_model"
		self.water_volume = "water_volume(l)"


		self.NoInformation = "NoInformation"

		self.path_services_json = "path_services_json"

		#self. = ""
		
		self.name = "name"
		self.localhost = "localhost"
		self.port = "port"
		self.ip = "ip"
		self.main_ip = "main_ip"
		self.main_port = "main_port"

		self.token_telegram_bot = "token_telegram_bot"
		
		self.world_path = "./data/stored/world.json"

		self.world_localities_path = "./ms_resource_catalog/data/world_locality.json"
		self.settings_path = "./settings.json"
		
		#self.cat_loc_1_PATH = "./data/stored/locality_catalog.json"
		#self.cat_cannons_1_PATH = "./data/stored/cannons_catalog.json"
		#self.cat_sensors_1_PATH = "./data/stored/sensors_catalog.json"
		
		self.cat_loc_1_PATH = "./data/stored_test/locality_catalog.json"
		self.cat_cannons_1_PATH = "./data/stored_test/cannons_catalog.json"
		self.cat_sensors_1_PATH = "./data/stored_test/sensors_catalog.json"
		
		self.data_recorded_path =  "./data/stored/data_recorded.json"
		
		self.path_end_cannons = "/cannons_catalog.json"
		self.path_end_sensors = "/sensors_catalog.json"
		self.path_end_locality = "/locality_catalog.json"
		self.path_end_history = "/history.json"

		#constant
		self.ID_default = 1
		
		self.FORMAT_INT = 0
		self.FORMAT_FLOAT = 1
		self.FORMAT_STRING = 2
		
		self.cannonTypesPossible = ["mobile,fisso"]
		self.cannonModePossible = ["auto","manual","off"]
		self.cannonStatePossible = ["off", "on"]


		# INFLUX_DB
		self.bucket_Io3_raw_data = "Io3_raw_data"
		self.bucket_Io3_processed_data = "Io3_processed_data"
		self.bucket_Io3_Test1 = "Io3_Test1"
		
	def print_name_cmd_2_lines(self):
		print(" \n\
				 _______  _        _______           ______   \n\
				(  ____ \( \      (  ___  )|\     /|(  __  \  \n\
				| (    \/| (      | (   ) || )   ( || (  \  ) \n\
				| |      | |      | |   | || |   | || |   ) | \n\
				| |      | |      | |   | || |   | || |   | | \n\
				| |      | |      | |   | || |   | || |   ) | \n\
				| (____/\| (____/\| (___) || (___) || (__/  ) \n\
				(_______/(_______/(_______)(_______)(______/")
