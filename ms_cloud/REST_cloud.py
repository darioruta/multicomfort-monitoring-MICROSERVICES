# file dedicato all'interfaccia REST 


import defines.defineJSONVariables as deJSONVar
import json
import cherrypy
import cherrypy_cors
import requests


import defines.defineExceptions as deExcept
import defineURIMicroservices as deMicroServices
from bibliotecario import bibliotecario
deMS = deMicroServices.de_microservices()

ex = deExcept.Exception()
de = deJSONVar.de()

class RESTCloudDefault():
	exposed = True

	def __init__(self, s):
		self.status = s
		pass
	@cherrypy.tools.json_out()
	def GET(self, *uri, **param):
		if (uri, list(param.keys()),) == deMS.main:
			if self.status:
				return "microservizio 'CLOUD' -> OK"
			else:
				return "ERROR PAGE -> CARICAMENTO 'CLOUD' NON RIUSCITO -> alcuni IDs si ripetono"
		return "ERROR PAGE -> microservizio 'CLOUD' non caricato correttamente"


class RESTCloud:
	exposed = True

	def __init__(self):
		self.bi = bibliotecario()
		pass

	def __init__(self, bibliotecario, localityName, localityID):
		self.bi = bibliotecario
		self.localityName = localityName
		self.localityID = localityID
		self.uris_available = deMS.show_allUris()

	def OPTIONS(self, *uri, **param):
		cherrypy.response.status = 200
		cherrypy_cors.preflight(allowed_methods=['GET', 'POST', 'OPTIONS'])
		return "OK"
	#@classmethod

	# turn ``return``ed Python object into a JSON string; also setting corresponding Content-Type
	@cherrypy.tools.json_out()
	def GET(self, *uri, **param):
		print("URL from cherrypy: " + str(cherrypy.url()))
		print("PARAM from cherrypy: " + str(param))
		print("PARAM.keys from cherrypy: " + str(list(param.keys())))
		#print(f"uri ricevuta: {uri}")
		cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
		#cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
		cherrypy.response.headers['Access-Control-Allow-Headers'] = "append,delete,entries,foreach,get,has,keys,set,values,Authorization"
		cherrypy.response.headers['Access-Control-Allow-Methods'] = "POST, GET, OPTIONS, DELETE, PUT"

		cherrypy.response.status = 200
		cherrypy_cors.preflight(allowed_methods=['GET', 'POST', 'OPTIONS'])

		# URI ALLOWED
		if (uri, list(param.keys()),) == deMS.main:
			return f"{self.localityName} -> mainPage -> correct built-in -> OK"
		if (uri, list(param.keys()),) == deMS.select:
			print("SELECT data from cloud")
			if not self.bi.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}
			info = self.bi.select(param[deMS.param_sensors].split(','), int(param[deMS.param_limit]), param[deMS.param_day_referred])
			if info == None :
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info
		if (uri, list(param.keys()),) == deMS.select_influxDB_base:
			print("SELECT data from cloud")
			#if not self.bi.ControlChecksum(int(param[deMS.param_checksum])):
			#	return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}
			info = self.bi.Read_Measurements_InfluxDB(fields = ["temp","co2"], bucket=de.bucket_Io3_Test1)
			if info == None :
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info
		if (uri, list(param.keys()),) == deMS.get_info_to_populate_cards:
			print("SELECT data from cloud")
			#if not self.bi.ControlChecksum(int(param[deMS.param_checksum])):
			#	return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}
			info = self.bi.RetrieveDataToPopulateCards(int(param[deMS.param_id_kit]), list(param[deMS.fields]))
			print(info)
			if info == None :
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info
		if (uri, list(param.keys()),) == deMS.get_storico_dati:    # -> /3/history/data?id=1&fields[]=a&fields[]=b
			print("SELECT data from cloud")
			print(param["fields[]"])
			#if not self.bi.ControlChecksum(int(param[deMS.param_checksum])):
			#	return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}
			info = self.bi.GetStoricoData(int(param[deMS.param_id_kit]), list(param[deMS.fields]), str(param[deMS.range_start]))
			if info == None:
				return {deMS.response: "ERROR RETRIVING INFORMATION"}
			return info
		elif (uri, list(param.keys()),) == deMS.GetAllOnlineKitsIDs:
			print(f'http://127.0.0.1:8082/{self.localityID}/kits/allonlineIDs')
			response = requests.get(f'http://127.0.0.1:8082/{self.localityID}/kits/allonlineIDs')
			d = response.json()
			d1 = d["KitsIDs"]
			print(f"RESPONSE: {d1}")
			return response.json()
			return json.loads(response.text)
		# ONLY FOR IMPLEMENTATION TIME
		elif (uri, list(param.keys()),) == True:
			print("")
			return True
		# CATCH URI NOT ALLOWED
		else:
			print(f"ERRORE: URI NON PRESENTE: {uri}")
			#print("ERRORE: URI NON PRESENTE")

			# per far ritornare un file di testo HTML
			cherrypy.response.headers['Content-Type'] = 'text/html'
			return f"<p> Page Not Found -> Uri or parameters not correct </p> {self.uris_available}"
			#return None


	@cherrypy.tools.json_in()
	# turn ``return``ed Python object into a JSON string; also setting corresponding Content-Type
	@cherrypy.tools.json_out()
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

		# URI ALLOWED
		if (uri, list(param.keys()),) == deMS.main:
			return "mainPage -> correct built-in -> OK"

		elif (uri, list(param.keys()),) == deMS.addMeasurements:
			print("Set Info Cannon By CannonID")
			if not self.bi.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}
			if self.bi.addMeasurements(cherrypy.request.json):
				return {deMS.response: "ERROR UPDATING NEW FEAURES"}
			return ex.DONE_CORRECT
		elif (uri, list(param.keys()),) == deMS.addMeasurements_influxDB:
			print("Set Info Cannon By CannonID")
			if not self.bi.ControlChecksum(int(param[deMS.param_checksum])):
				return {deMS.response: "ERRORE CHECKSUM NON VALIDO"}
			data = cherrypy.request.json
			measurements = data["data"]
			tags = [ ("kitID", data["kitID"])]
			if self.bi.addMeasurements_InfluxDB(measurements, tags ,bucket=de.bucket_Io3_raw_data, timestamp= data["timestamp"]):
				return {deMS.response: "ERROR UPDATING NEW FEAURES"}
			return ex.DONE_CORRECT
		# ONLY FOR IMPLEMENTATION TIME
		elif (uri, list(param.keys()),) == True:
			print("")
			return True
		else:
			print("ERROR URI DELETE NOT PRESENT")
			return "Page Not Found -> Uri or parameters not correct"
			#return None

	# turn ``return``ed Python object into a JSON string; also setting corresponding Content-Type
	@cherrypy.tools.json_out()
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
		if (uri, list(param.keys()),) == deMS.main:
			return "mainPage -> correct built-in -> OK"
		# ONLY FOR IMPLEMENTATION TIME
		elif (uri, list(param.keys()),) == True:
			print("")
			return True
		else:
			print("ERROR URI DELETE NOT PRESENT")
		return "Page Not Found -> Uri or parameters not correct"
	
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
		if (uri, list(param.keys()),) == deMS.main:
			return "mainPage -> correct built-in -> OK"
		# ONLY FOR IMPLEMENTATION TIME
		elif (uri, list(param.keys()),) == True:
			print("")
			return True
		else:
			print("ERROR URI DELETE NOT PRESENT")
			return "Page Not Found -> Uri or parameters not correct"
			#return None
	#@cherrypy.tools.json_in()
