import defines.defineExceptions as deExcept
import json
import cherrypy
import cherrypy_cors
#import requests

import burattinaio

# import json variable names under the variable de
import defines.defineURIMicroservices as deMicroServices
deMS = deMicroServices.de_microservices()

# import json variable names under the variable de
# NON UTILIZZATO PER ORA 
import defines.defineJSONVariables as deJSONVar
de = deJSONVar.de()

ex = deExcept.Exception()


class REST_resource_catalog_default():
	exposed = True

	def __init__(self, s):
		self.status = s
		self.uris_available = deMS.show_allUris()
		pass
	@cherrypy.tools.json_out()
	def GET(self, *uri, **param):	
		
		if (uri, list(param.keys()),) == deMS.main:
			if self.status:
				# per far ritornare un file di testo HTML
				cherrypy.response.headers['Content-Type'] = 'text/html'
				return f"<p>microservizio '{__class__.__name__}' -> OK</p> {self.uris_available}"
			else:
				return f"ERROR PAGE -> {__class__.__name__} loading FAILED"
		elif (uri, list(param.keys()),) == deMS.getTokenTelegramBot:
			print("Get Token Telegram Bot")
			f = open("./data/world_locality.json", "r")
			print(f)
			world_settings = json.load(f)
			f.close()
			info = world_settings[de.token_telegram_bot]
			if info == None:
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info
		return "ERROR PAGE -> microservizio 'RESTSlopeService' non caricato correttamente"




class REST_resource_catalog:
	exposed = True
	def __init__2(self):
		self.bu = burattinaio.burattinaio()
		pass
	def __init__(self, burattinaio):
		self.bu = burattinaio 
		self.uris_available = deMS.show_allUris()
	def OPTIONS(self, *uri, **param):
		cherrypy.response.status = 200
		cherrypy_cors.preflight(allowed_methods=['GET', 'POST', 'OPTIONS'])
		return "OK"
	#@classmethod
	@cherrypy.tools.json_out()  # turn ``return``ed Python object into a JSON string; also setting corresponding Content-Type
	def GET(self, *uri, **param):
		print("URL from cherrypy: " + str(cherrypy.url()))
		print("PARAM from cherrypy: " + str(param))	
		print("PARAM.keys from cherrypy: " + str(list(param.keys())))
		print(uri)
		cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
		#cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
		cherrypy.response.headers['Access-Control-Allow-Headers'] = "append,delete,entries,foreach,get,has,keys,set,values,Authorization"
		cherrypy.response.headers['Access-Control-Allow-Methods'] = "POST, GET, OPTIONS, DELETE, PUT"
  
		cherrypy.response.status = 200
		cherrypy_cors.preflight(allowed_methods=['GET', 'POST', 'OPTIONS'])

		# URI ALLOWED
		if (uri, list(param.keys()),) == deMS.main:
			return f"{self.bu.GetInfoLocality()[de.localityName]} -> mainPage -> correct built-in -> OK"

		#--------------------------------------------
		#			RETRIEVE CATALOGUE JSON
		#--------------------------------------------
		elif (uri, list(param.keys()),) == deMS.GetAllCannonCatalogue:
			print("Get Cannon Catalog")
			# TODO verificare che il parametro id sia un intero
			info = self.bu.GetAllCannonCatalogue()
			if info == None:
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info

		elif (uri, list(param.keys()),) == deMS.GetAllKitCatalogue:
			print("Get Kit Catalog")
			# TODO verificare che il parametro id sia un intero
			info = self.bu.GetAllKitCatalogue()
			if info == None:
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info

		elif (uri, list(param.keys()),) == deMS.GetAllLocalityCatalogue:
			print("Get Info Locality")
			# TODO verificare che il parametro id sia un intero
			info = self.bu.GetAllLocalityCatalogue()
			if info == None:
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info
		
		#--------------------------------------------
		#			RETRIEVE INFO 
		#--------------------------------------------
		
		elif (uri, list(param.keys()),) == deMS.GetInfoLocality:
			print("Get Info Locality")
			# TODO verificare che il parametro id sia un intero
			info = self.bu.GetInfoLocality(int(param[deMS.param_num_slopes]))
			if info == None:
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info
		
		elif (uri, list(param.keys()),) == deMS.GetPlessiStructure:
			print("Get Plessi Structure")
			# TODO verificare che il parametro id sia un intero
			info = self.bu.GetPlessiStructure()
			if info == None:
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info

		elif (uri, list(param.keys()),) == deMS.GetAllPlessiIDs:
			print("Get All Plessi")
			info = self.bu.GetAllPlessiID()
			if info == None:
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info
		
		elif (uri, list(param.keys()),) == deMS.GetAllAuleIDsinPlessoID:
			print("Get All Aule in PlessoID")
			info = self.bu.GetAllAuleIDinPlessoID(int(param[deMS.param_id]))
			if info == None:
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info

		elif (uri, list(param.keys()),) == deMS.GetAllCannonsIDs:
			print("Get All Cannons IDs")
			info = self.bu.GetAllCannonsIDs()
			if info == None :
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info

		elif (uri, list(param.keys()),) == deMS.GetAllKitsIDs:
			print("Get All Kits IDs")
			info = self.bu.GetAllKitsIDs()
			if info == None :
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info
		elif (uri, list(param.keys()),) == deMS.GetAllOnlineKitsIDs:
			print("Get All Kits IDs")
			info = self.bu.GetAllOnlineKitsIDs()
			print(info)
			if info == None:
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info

		elif (uri, list(param.keys()),) == deMS.GetAllCannonsIDsInSectorIDandSlopeID:
			print("Get All Cannons IDs in slopeID and sectorID")
			info = self.bu.GetAllCannonsIDsInSectorIDandSlopeID(param[deMS.param_id], param[deMS.param_id_2])
			if info == None:
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info

		elif (uri, list(param.keys()),) == deMS.GetAllKitsIDsInAulaIDandPlessoID:
			print("Get All Sensors IDs in slopeID and sectorID")
			info = self.bu.GetAllSensorsIDsInSectorIDandSlopeID(param[deMS.param_id], param[deMS.param_id_2])
			if info == None:
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info

		elif (uri, list(param.keys()),) == deMS.GetInfoCannonByCannonID:
			print("Get Info Cannon By Cannon ID")
			# TODO verificare che il parametro id sia un intero
			info = self.bu.GetInfoCannonByCannonID(int(param[deMS.param_id]))
			if info == None :
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info

		elif (uri, list(param.keys()),) == deMS.GetInfoKitByKitID:
			print("Get Info Sensor By Sensor ID")
			# TODO verificare che il parametro id sia un intero
			info = self.bu.GetInfoSensorBySensorID(int(param[deMS.param_id]))
			if info == None :
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info
		
		# ONLY FOR IMPLEMENTATION TIME
		elif (uri, list(param.keys()),) == True:
			print("")
			return True
		# CATCH URI NOT ALLOWED
		else:
			print("ERRORE: URI NON PRESENTE")

			# per far ritornare un file di testo HTML
			cherrypy.response.headers['Content-Type'] = 'text/html'
			return f"<p> Page Not Found -> Uri or parameters not correct </p> {self.uris_available}"
			#return None

	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()  # turn ``return``ed Python object into a JSON string; also setting corresponding Content-Type
	def PUT(self, *uri, **param):
		print("URL from cherrypy: " + str(cherrypy.url()))
		print("PARAM from cherrypy: " + str(param))	
		print("PARAM.keys from cherrypy: " + str(list(param.keys())))
		print(uri)
		cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
		#cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
		cherrypy.response.headers['Access-Control-Allow-Headers'] = "append,delete,entries,foreach,get,has,keys,set,values,Authorization"
		cherrypy.response.headers['Access-Control-Allow-Methods'] = "POST, GET, OPTIONS, DELETE, PUT"
  
		cherrypy.response.status = 200
		cherrypy_cors.preflight(allowed_methods=['GET', 'POST', 'OPTIONS'])

		#--------------------------------------------
		#			SET INFO
		#--------------------------------------------
  
		# URI ALLOWED
		if (uri, list(param.keys()),) == deMS.SetInfoCannonByCannonID:
			print("Set Info Cannon By CannonID")
			if not self.bu.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}
			if self.bu.SetInfoCannonByCannonID(cherrypy.request.json):
				return {deMS.response: "ERROR UPDATING NEW FEAURES"}
			return ex.DONE_CORRECT

		elif (uri, list(param.keys()),) == deMS.SetInfoKitByKitID:
			print("Set Info Kit By KitID")
			if not self.bu.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}	
			
			if self.bu.SetInfoKitByKitID(cherrypy.request.json):
				return {deMS.response: "ERROR UPDATING NEW FEAURES"}
			return ex.DONE_CORRECT

		elif (uri, list(param.keys()),) == deMS.AddCannonToSlopeSector:
			print("Add Cannon by cannonID to Plesso-Aula")
			if not self.bu.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}	
			
			if self.bu.AddCannonToSlopeSector(int(param[deMS.param_id]), int(param[deMS.param_id_2]), int(param[deMS.param_id_3])):
				return {deMS.response: "ERROR UPDATING NEW FEAURES"}
			return ex.DONE_CORRECT
		elif (uri, list(param.keys()),) == deMS.AddKitToPlessoAula:
			print("Add Kit By KitID into Plesso-Aula")
			if not self.bu.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}	
			
			if self.bu.AddKitToPlessoAula(int(param[deMS.param_id]), int(param[deMS.param_id_2]),  int(param[deMS.param_id_3])):
				return {deMS.response: "ERROR UPDATING NEW FEAURES"}
			return ex.DONE_CORRECT
		elif (uri, list(param.keys()),) == deMS.Put_Ping_Device_Catalog:
			print("Add Kit By KitID into Plesso-Aula")
			#if not self.bu.ControlChecksum(int(param[deMS.param_checksum])):
			#	return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}
			dat = cherrypy.request.json
			dev_name = list(dat.keys())[0]
			t = dat[dev_name]
			if self.bu.Update_Ping_Device_Catalog(dev_name,t):
				return {deMS.response: "ERROR UPDATING NEW FEAURES"}
			return ex.DONE_CORRECT
		else:
			print("ERROR URI DELETE NOT PRESENT")
			# per far ritornare un file di testo HTML
			cherrypy.response.headers['Content-Type'] = 'text/html'
			return f"<p> Page Not Found -> Uri or parameters not correct </p> {self.uris_available}"

			#return None

	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()  # turn ``return``ed Python object into a JSON string; also setting corresponding Content-Type
	def POST(self, *uri, **param):
		print("URL from cherrypy: " + str(cherrypy.url()))
		print("PARAM from cherrypy: " + str(param))	
		print("PARAM.keys from cherrypy: " + str(list(param.keys())))
		print(uri)
		cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
		#cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
		cherrypy.response.headers['Access-Control-Allow-Headers'] = "append,delete,entries,foreach,get,has,keys,set,values,Authorization"
		cherrypy.response.headers['Access-Control-Allow-Methods'] = "POST, GET, OPTIONS, DELETE, PUT"
  
		cherrypy.response.status = 200
		cherrypy_cors.preflight(allowed_methods=['GET', 'POST', 'OPTIONS'])
		# URI ALLOWED
		if (uri, list(param.keys()),) == deMS.AddNewCannon:
			print("Add New Cannon")
			if not self.bu.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}	
			if self.bu.AddNewCannon():
				return {deMS.response: "ERROR CREATING NEW OBJECT"}
			# TODO far ritornare il cannonID creato, altrimenti non ho idea di che ID abbia il nuovo oggetto
			return ex.DONE_CORRECT

		elif (uri, list(param.keys()),) == deMS.AddNewKit:
			print("Add New Kit")
			if not  self.bu.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}	

			if self.bu.AddNewSensor(cherrypy.request.json):
				return {deMS.response: "ERROR CREATING NEW OBJECT"}
			# TODO far ritornare il sensorID creato, altrimenti non ho idea di che ID abbia il nuovo oggetto
			return ex.DONE_CORRECT

		elif (uri, list(param.keys()),) == deMS.AddNewPlesso:
			print("Add New Plesso")
			if not  self.bu.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}	

			if self.bu.AddNewSlope():
				return {deMS.response: "ERROR CREATING NEW OBJECT"}
			# TODO
			return ex.DONE_CORRECT

		elif (uri, list(param.keys()),) == deMS.AddNewAulaToPlesso:
			print("Add New Aula To Sector")
			if not self.bu.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}	

			if self.bu.AddNewSectorToSlope(int(param[deMS.param_id])):
				return {deMS.response: "ERROR CREATING NEW OBJECT"}
			# TODO
			return ex.DONE_CORRECT
		else:
			print("ERROR URI DELETE NOT PRESENT")
		# per far ritornare un file di testo HTML
		cherrypy.response.headers['Content-Type'] = 'text/html'
		return f"<p> Page Not Found -> Uri or parameters not correct </p> {self.uris_available}"


	# turn ``return``ed Python object into a JSON string; also setting corresponding Content-Type

	@cherrypy.tools.json_out()
	def DELETE(self, *uri, **param):
		print("URL from cherrypy: " + str(cherrypy.url()))
		print("PARAM from cherrypy: " + str(param))
		print("PARAM.keys from cherrypy: " + str(list(param.keys())))
		print(uri)
		cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
		#cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
		cherrypy.response.headers['Access-Control-Allow-Headers'] = "append,delete,entries,foreach,get,has,keys,set,values,Authorization"
		cherrypy.response.headers['Access-Control-Allow-Methods'] = "POST, GET, OPTIONS, DELETE, PUT"

		cherrypy.response.status = 200
		cherrypy_cors.preflight(allowed_methods=['GET', 'POST', 'OPTIONS'])

		# URI ALLOWED
		if (uri, list(param.keys()),) == deMS.DropCannonByCannonID:
			print("Drop Cannon By CannonID")
			if not self.bu.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}
			if self.bu.DropCannonByCannonID(int(param[deMS.param_id])):
				return {deMS.response: "ERROR DELETING OBJECT"}
			return ex.DONE_CORRECT

		elif (uri, list(param.keys()),) == deMS.DropKitByKitID:
			print("Drop Kit By KitID")
			if not self.bu.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}
			if self.bu.DropKitByKitID(int(param[deMS.param_id])):
				return {deMS.response: "ERROR DELETING OBJECT"}
			return ex.DONE_CORRECT

		elif (uri, list(param.keys()),) == deMS.DropPlessoByPlessoID:
			print("Drop Plesso By PlessoID")
			if not self.bu.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}

			if self.bu.DropPlessoByPlessoID(int(param[deMS.param_id])):
				return {deMS.response: "ERROR DELETING OBJECT"}
			return ex.DONE_CORRECT

		elif (uri, list(param.keys()),) == deMS.DropAulaByAulaIDAndPlessoID:
			print("Drop Aula By AulaID And PlessoID")
			if not self.bu.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}

			if self.bu.DropAulaByAulaIDAndPlessoID(int(param[deMS.param_id]), int(param[deMS.param_id_2])):
				return {deMS.response: "ERROR DELETING OBJECT"}
			return ex.DONE_CORRECT
		else:
			print("ERROR URI DELETE NOT PRESENT")
			# per far ritornare un file di testo HTML
			cherrypy.response.headers['Content-Type'] = 'text/html'
			return f"<p> Page Not Found -> Uri or parameters not correct </p> {self.uris_available}"
			#return None
