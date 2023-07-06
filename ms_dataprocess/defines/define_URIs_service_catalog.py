class de_microservices ():
	
	'''

	Class dedicated to 'store' globals definitions of variables

	'''

	def __init__(self):
		self.param_id= "id"
		self.param_id_2 = "id2"
		self.param_id_3 = "id3"
		self.param_num_slopes = "ns"
		self.param_info = "info"
		self.param_checksum = "cks"
		self.state = "state"
		
		self.response = "response"
		self.main = ((), [])
		self.set_status = (("set_status",), [self.state])
		self.set_status_base = (("set_status_base",), [self.state])
		self.set_status_kpi = (("set_status_kpi",), [self.state])
		
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
