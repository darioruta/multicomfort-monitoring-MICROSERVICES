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
		self.main = ((),[],)

		self.getTokenTelegramBot = (("token_telegram_bot",), [],)

		self.GetAllCannonCatalogue = (("locality","cannonCatalogue"), [],)
		self.GetAllKitCatalogue = (("locality","kitCatalogue"), [],)
		self.GetAllLocalityCatalogue = (("locality", "localityCatalogue"), [],)

		self.GetInfoLocality = (("localityInfo",), [self.param_num_slopes],)
		self.GetPlessiStructure = (("locality", "plessiStructure"), [],)
		self.GetAllPlessiIDs = (("plessiInfo",), [],)
		self.GetAllAuleIDsinPlessoID = (("plesso", "allAule"), [self.param_id],)

		self.GetAllKitsIDs = (("kits", "allIDs",), [],)
		self.GetAllOnlineKitsIDs = (("kits", "allonlineIDs",), [],)
		self.GetAllCannonsIDs = (("cannons", "allIDs",), [],)

		self.GetAllKitsIDsInAulaIDandPlessoID = (("plesso", "aula","kits"), [self.param_id, self.param_id_2],)
		self.GetAllCannonsIDsInSectorIDandSlopeID = (("plesso", "aula","cannons"), [self.param_id, self.param_id_2],)
		
		self.GetInfoKitByKitID = (("kit", "info"), [self.param_id],)
		self.GetInfoCannonByCannonID = (("cannon", "info"), [self.param_id],)

		self.SetInfoKitByKitID = (("kit","setInfo",),[ self.param_checksum])
		self.SetInfoCannonByCannonID = (("cannon", "setInfo",), [self.param_checksum])
		
		self.AddKitToPlessoAula = (("kit", "moveTo",), [self.param_id, self.param_id_2, self.param_id_3, self.param_checksum])
		self.AddCannonToSlopeSector = (("cannon", "moveTo",), [
		                               self.param_id, self.param_id_2, self.param_id_3, self.param_checksum])


		self.DropCannonByCannonID = (("cannon", "drop",), [self.param_id, self.param_checksum])
		self.DropKitByKitID = (("kit", "drop",), [self.param_id, self.param_checksum])
		self.DropPlessoByPlessoID = (("plesso", "drop",), [self.param_id, self.param_checksum])
		# id => plessoID, id2 => aulaID
		self.DropAulaByAulaIDAndPlessoID = (("plessoAula","drop",), [self.param_id, self.param_id_2, self.param_checksum])
		

		self.AddNewPlesso = (("plessi", "new",), [self.param_checksum])
		self.AddNewAulaToPlesso = (("plesso", "aule", "new",), [self.param_id, self.param_checksum])
		self.AddNewKit = (("kits", "new",), [self.param_checksum])
		self.AddNewCannon = (("cannons", "new",), [self.param_checksum])

		self.Put_Ping_Device_Catalog = (("ping_res",),[])
		
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
			if len(params) >0:
				mess += "?"
				for v in params:
					mess+= v + "= VALUE &"
				mess = mess[:-1]
			final += f"{attribute} => &nbsp&nbsp&nbsp&nbsp {mess}<br><br>"
			
			print(attribute, '=>\t\t', mess)
		return final

		
		