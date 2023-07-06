from ast import Param


class de_microservices ():
	
	'''

	Class dedicated to 'store' globals definitions of variables

	'''

	def __init__(self):

		self.param_id = "id"
		self.param_id_kit = "id_kit"
		self.param_id_user = "id_user"
		self.param_id_2 = "id2"
		self.param_id_3 = "id3"
		self.param_num_slopes = "ns"
		self.param_info = "info"
		self.param_checksum = "cks"
		self.param_sensors = "s"
		self.param_limit = 'l'
		self.param_day_referred = 'dr'
		self.param_timestamp = "t"
		self.param_values = 'v'
		self.fields = "fields[]"
		self.range_start = "rs"

		self.response = "response"
		#SELECT
		self.main = ((), [],)
		self.select = (('hystory','sensors'),[self.param_sensors,self.param_limit, self.param_day_referred, self.param_checksum])
		self.select_influxDB = (('hystory','kits'),[self.param_sensors,self.param_limit, self.param_day_referred, self.param_checksum])
		self.select_influxDB_base = (('history','base'),[])
		self.get_info_to_populate_cards = (('history', 'cards'), [ self.param_id_kit, self.fields ])

		# -> /3/history/data?id=1&fields[]=a&fields[]=b    -> PER CREARE VETTORI NELLE URI
		self.get_storico_dati = (('history', 'data'), [self.param_id_kit, self.fields, self.range_start])

		self.GetAllOnlineKitsIDs = (("kits", "allonlineIDs",), [],)
		
		# PUT
		self.addMeasurements = (('history','new'), [self.param_checksum],) #-> indo passate nel json
		self.addMeasurements_influxDB = (('history','new_influxDB'), [self.param_checksum],) #-> indo passate nel json
		self.startAutoGenerationData = (('history','startGeneration'), [self.param_checksum],) #-> indo passate nel json
		self.stopAutoGenerationData = (('history','stopGeneration'), [self.param_checksum],) #-> indo passate nel json
		
	def show_allUris(self):
		final = "<p>"
		for attribute, value in self.__dict__.items():

			if not type(value) is tuple:
				continue
			uri = [u for u in value[0]]
			params = value[1]
			mess = "localhost/ &nbsp&nbsp 'localityID'/ &nbsp&nbsp"
			for u in uri:
				mess += u + "/"
			mess = mess[:-1]
			if len(params) > 0:
				mess += "?"
				for v in params:
					mess += v + "= VALUE &"
				mess = mess[:-1]
			final += f"{attribute} => &nbsp&nbsp&nbsp&nbsp {mess}<br><br>"

			print(attribute, '=>\t\t', mess)
		return final


		
		