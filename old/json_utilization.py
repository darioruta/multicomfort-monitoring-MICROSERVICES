# created on 16-12-2021
# Davide Montrucchio 
#
import json
import defines.defineJSONVariables as deJSONVar
de = deJSONVar.de()

class JsonMethods ():
	"""Class dedicated to store, visualize, dumps json file

	Parameters
	----------
	fromJSONFile(.json) : json file in input

	"""
	def __init__(self, fromJSONFile = False):
		if (fromJSONFile == False):
			# inizializzo a nulla il data
			self.data = {}
			print("JSON inizializzato a vuoto")
		else:
			# altrimenti apro il file
			self.jsonFile = fromJSONFile
			with open(self.jsonFile) as f:
				self.data = json.load(f)
				f.close()
				print(f"file JSON: {self.jsonFile} -> caricato correttamente, chiuso correttamente")
				return 
			print("Fine JSON non trovato")
	def dumpsJson(self,jsonFileOutput = ""):
		""" Function dedicated to dump the json into a proper file

		Parameters
		----------
		jsonFileOutput(.json) : destination path where store the json modified

		"""
		if jsonFileOutput == "":
			jsonFileOutput = self.jsonFile
		with open(jsonFileOutput,'w') as f:
			f.write( json.dumps(self.data))
			f.close()
			print(f"file JSON: {self.jsonFile} -> aggiornato correttamente -> chiuso correttamente" )
			return True
		print(f"ERROR SAVING JSON INTO FILE: {self.jsonFile}")
		return False
	def ricors (self, e,n_t, last):
		"""Function dedicated to the ricorsion into the element of the json file

		Parameters
		----------
		element : element cosidered 
		n_t : number of tabs used to display nested objects
		last : information of the parent object 
		
		"""
		if last == list:
			if isinstance(e,list):
				print("\t" * n_t + "[")
				n_t= n_t +1
				for k1 in e:
					self.ricors(k1,n_t, list)
				print("\t" * n_t + "]")
			elif  isinstance(e,dict):
				print("\t" * n_t + "{")
				n_t= n_t +1
				for e1 in e.items():
					self.ricors(e1,n_t, dict)
				print("\t" * (n_t-1) + "},")
			else:
				print("\t" * n_t + str(e)  + " ,")
		elif last == dict:

			if isinstance(e[1],list):
				print("\t" * n_t + str(e[0])+ ": [")
			
				n_t= n_t +1
				for k1 in e[1]:
					self.ricors(k1,n_t, list)
				print("\t" * n_t + "]")
			elif  isinstance(e[1],dict):
				print("\t" * n_t + str(e[0]) + ":{")
				n_t= n_t +1
				for e1 in e[1].items():
					self.ricors(e1,n_t, dict)
				print("\t" * (n_t -1) + "}")
			else :
				print("\t" * n_t + str(e[0])+ ": " + str(e[1]) + " ,")
			
		else:
			print("\t" * n_t + "problems")
			
	def ToString(self):
		"""Function dedicated to display the json information

		"""
		tab = "\t";
		n_tabs = 1;
		print("Json Data: {")
		for el in self.data.items():
			self.ricors(el,n_tabs , dict)
		print( "}")
				

class JsonMethodsCreateDataSensor(JsonMethods):
	def CreateJson(self, sensorID, slopeID, temperature, humidity, deepsensor, timestamp):
		self.data =  SensorDataFormat().CreateSensorDataFormat(sensorID, temperature, humidity, deepsensor, timestamp)
	
		self.AddSlopeID( slopeID)
 
	def AddSlopeID(self, slopeID):
		self.data[de.slopeID] = slopeID

class SensorDataFormat():
	def CreateMeasurement(self,temperature , humidity,deepsensor , timestamp):
		mis = {}
		mis[de.temperature] = temperature
		mis[de.humidity] = humidity
		mis[de.deepsensor] = deepsensor
		mis[de.timestamp] =  timestamp
		return mis
	def CreateSensorDataFormat(self,sensorID = -1, temperature = [], humidity = [], deepsensor = [], timestamp = "" ):
		sensor = {}
		sensor[de.sensorID] = sensorID
		sensor[de.data] = self.CreateMeasurement(temperature , humidity,deepsensor , timestamp)
		return sensor

class SlopeDataFormat():
	def CreateSlope(self, slopeID = -1 ):
		slope = {}
		slope[de.slopeID] = slopeID
		# lista possibile di sensori per ora vuota perché la stiamo inizializzando
		slope[de.sectors] = []
	
class LocalityDataFormat():
	def __init__(self, localityID):
		loc = {}
		#la localitá viene creata solo con il locality ID, tutte le altre info si aggiungono dopo
		loc[de.localityID] = localityID
		loc[de.info] = self.CreateInfoLoc()
		loc[de.slopes] = []
	def CreateInfoLoc(self):
		info = {}
		info[de.localityName] = de.NoInformation
		info[de.mslm] = de.NoInformation
		return info



class JsonMethodsCreateSlope(JsonMethods):
	def CreateSlope(self, slope):
		print("cc")


if __name__== "__main__":
	data = JsonMethods("json_test.json")
	print(data.ToString())

