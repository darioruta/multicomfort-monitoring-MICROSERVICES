# created on 16-12-2021
# Davide Montrucchio 
#
import json

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
			#print("JSON inizializzato a vuoto")
		else:
			# altrimenti apro il file
			self.jsonFile = fromJSONFile
			with open(self.jsonFile) as f:
				self.data = json.load(f)
				f.close()
				#print(f"file JSON: {self.jsonFile} -> caricato correttamente, chiuso correttamente")
				return 
			#print("Fine JSON non trovato")
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
			#print(f"file JSON: {self.jsonFile} -> aggiornato correttamente -> chiuso correttamente" )
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
				


if __name__== "__main__":
	data = JsonMethods("json_test.json")
	print(data.ToString())

