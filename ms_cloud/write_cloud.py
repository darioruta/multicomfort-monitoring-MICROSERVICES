import defines.defineExceptions as deExcept


# import json variable names under the variable de
from defineVariable import de as defineVariable
de = defineVariable()


import sys
#sys.path.append('D:\\POLITECNICO\\Magistrale\\A_IP\\project\\codice')
import json_utilization as ju
import lib1 
class ControlInputParameter:
	def Verify_some_inputs(self):
		print("qua faccio dei controlli per verificare che quello che si vuole aggiungere al cloud abbia senso")
	# esempio
	def VerifyLocalityInfo(self, locName, mslm):
		if lib1.check_user_input(locName, de.FORMAT_STRING) and \
				lib1.check_user_input(mslm, de.FORMAT_INT):
			return True
		else:
			print(f"input non corretti! \n \
			\t {de.localityName} -> STRING \n \
			\t {de.mslm} -> INT \n ")
			return False

	def Verify_IDs_presence(self, values, total_possible_IDs):
		#tot_ok = True
		presenti = []
		assenti = []
		for i,v in enumerate(values):
			if  v[de.sensorID] in total_possible_IDs:
				presenti.append(v)
			else:
				assenti.append(v)
		#print(f"presenti: {presenti}, assenti: {assenti}")
		return  presenti,assenti
				

# il cloud é l'insieme di dati (misurazioni) salvati e disponibili nel tempo
class WriteCloud:
	def __init__(self, cloud_path):
		self.cloud_path = cloud_path
    # metodi riservati alla scrittura di dati presenti all'interno del cloud
	def createValue(self, sensorID, values):
		# values = {"t": 23 , "h": 45 ...}
		return {sensorID: values}

	def addMeasurement(self, timestamp, values ):
		cloud = ju.JsonMethods(fromJSONFile=self.cloud_path)
		cloud_history = cloud.data
		new_element = {de.timestamp: timestamp, de.values: values}
		cloud_history[de.history].append(new_element)
		cloud.dumpsJson()
		print(
		    f"\t Aggiunta nuova misuraone: timestamp: {timestamp}, values: {values}")
