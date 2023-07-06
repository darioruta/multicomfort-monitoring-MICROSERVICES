
# import json variable names under the variable de
import defines_shared.defineJSONVariables as deJSONVar
de = deJSONVar.de()

import json_utilization as ju



class ManageWorld:
	def __init__(self, file_world_path):
		self.path = file_world_path

	def NameLocalityByLocalityID(self, localityID):
		w = ju.JsonMethods(fromJSONFile=self.path).data
		for l in w[de.localities]:
			if l[de.localityID] == localityID:
				return l[de.localityName]
	
		return "ERRORE"
			
	def GetPathByLocalityID(self, localityID):
		w = ju.JsonMethods(fromJSONFile=self.path).data
		list_locID = [l[de.localityID] for l in w[de.localities]]
		if localityID not in list_locID:
			print("localityID requested NOT present")
			return False
		else:
			return w[de.localities][list_locID.index(localityID)][de.path], w[de.localities][list_locID.index(localityID)][de.localityID]
