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
		self.GetAllSensorCatalogue = (("locality","sensorCatalogue"), [],)
		self.GetAllLocalityCatalogue = (("locality", "localityCatalogue"), [],)

		self.GetInfoLocality = (("localityInfo",), [self.param_num_slopes],)
		self.GetSlopesStructure = (("locality", "slopesStructure"), [],)
		self.GetAllSlopeIDs = (("slopesInfo",), [],)
		self.GetAllSectorIDsinSlopeID = (("slope", "allSectors"), [self.param_id],)
		self.GetAllCannonsIDs = (("cannons","allIDs",), [],)
		self.GetAllSensorsIDs = (("sensors", "allIDs",), [],)

		self.GetAllCannonsIDsInSectorIDandSlopeID = (("slope", "sector","cannons"), [self.param_id, self.param_id_2],)
		self.GetAllSensorsIDsInSectorIDandSlopeID = (("slope", "sector","sensors"), [self.param_id, self.param_id_2],)

		self.GetInfoSensorBySensorID = (("sensor", "info"), [self.param_id],)
		self.GetInfoCannonByCannonID = (("cannon", "info"), [self.param_id],)	

		self.SetInfoCannonByCannonID = (("cannon","setInfo",),[ self.param_checksum])
		self.SetInfoSensorBySensorID = (("sensor","setInfo",),[ self.param_checksum])
		self.AddCannonToSlopeSector = (("cannon", "moveTo",), [self.param_id, self.param_id_2, self.param_id_3, self.param_checksum])
		self.AddSensorToSlopeSector = (("sensor", "moveTo",), [self.param_id, self.param_id_2, self.param_id_3, self.param_checksum])
		
		
  		#self.SetInfoCannonByCannonID = (("cannon","setInfo",),[self.param_info, self.param_checksum])
		#self.SetInfoSensorBySensorID = (("sensor","setInfo",),[self.param_info, self.param_checksum])



		self.DropCannonByCannonID = (("cannon", "drop",), [self.param_id, self.param_checksum])
		self.DropSensorBySensorID = (("sensor", "drop",), [self.param_id, self.param_checksum])
		self.DropSlopeBySlopeID = (("slope", "drop",), [self.param_id, self.param_checksum])
		# id => slopeID, id2 => sectorID
		self.DropSectorBySectorIDAndSlopeID = (("slopeSector","drop",), [self.param_id, self.param_id_2, self.param_checksum])
		

		self.AddNewSlope = (("slopes", "new",), [self.param_checksum])
		self.AddNewSectorToSlope = (("slope", "sectors", "new",), [self.param_id, self.param_checksum])
		self.AddNewSensor = (("sensors", "new",), [self.param_checksum])
		self.AddNewCannon = (("cannons", "new",), [self.param_checksum])
		

		
		