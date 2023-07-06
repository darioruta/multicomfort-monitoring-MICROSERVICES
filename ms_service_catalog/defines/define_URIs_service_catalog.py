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
		
		self.response = "response"
		self.main = ((), [])
		self.get_service_uri_by_name = (("get",), [self.param_id])

		self.put_service_ping = (("ser",), [])
		

		
		