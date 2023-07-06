class de ():
	
	'''

	Class dedicated to 'store' globals definitions of variables

	'''

	def __init__(self):
		self.temperature = "temperature"
		self.humidity = "humidity"
		self.deep = "deep"
		self.sensors = "sensors"
		self.sensorID = "sensorID"
		self.localityID = "localityID"
		self.info = "info"
		self.max = "max"
		self.min = "min"
		self.maxIncrement = "maxIncrement"
		self.variance = "variance"
		self.value = "value"
		self.localhost = "localhost"
		self.port = "port"
		self.t = "t"
		self.h = "h"
		self.d = "d"
		self.timestamp = "timestamp"
		self.name = "name"

		self.main_ip = "main_ip"
		self.main_port = "main_port"

	# link della pagina... https://www.askapache.com/online-tools/figlet-ascii/
	def print_name_cmd_2_lines(self):
		print(" \n\
         _______ _________ _______           _        _______ _________ _______  _______   \n\
        (  ____ \\\\__   __/(       )|\     /|( \      (  ___  )\__   __/(  ___  )(  ____ )  \n\
        | (    \/   ) (   | () () || )   ( || (      | (   ) |   ) (   | (   ) || (    )|  \n\
        | (_____    | |   | || || || |   | || |      | (___) |   | |   | |   | || (____)|  \n\
        (_____  )   | |   | |(_)| || |   | || |      |  ___  |   | |   | |   | ||     __)  \n\
              ) |   | |   | |   | || |   | || |      | (   ) |   | |   | |   | || (\ (     \n\
        /\____) |___) (___| )   ( || (___) || (____/\| )   ( |   | |   | (___) || ) \ \__  \n\
        \_______)\_______/|/     \|(_______)(_______/|/     \|   )_(   (_______)|/   \__/  \n")