

import json
import os
# import json variable names under the variable de
from defineVariable import de as defineVariable
de = defineVariable()

import sys
#sys.path.append('D:\\POLITECNICO\\Magistrale\\A_IP\\project\\codice')
sys.path.append(os.path.abspath(os.getcwd()))
import json_utilization as ju
import lib1 

# il cloud é l'insieme di dati (misurazioni) salvati e disponibili nel tempo
class ReadCloud:
	def __init__(self, cloud_path):
		self.cloud_path = cloud_path
    # metodi riservati alla lettura di dati presenti all'interno del cloud
	
	# get data
	def select(self, sensors = de.ALLsensors, limit = de.limit_DEFAULT, day_referred = False ):
		# day_referred => da quale giorno si deve iniziare a prendere le misurazioni richieste
		# ritorna un oggetto del tipo: 
		cloud = ju.JsonMethods(fromJSONFile=self.cloud_path).data
		print(f"Cloud/history: {cloud[de.history]}")
		timestamps = []
		values= dict()
		# se sono richieste piú del limite massimo permesso ne ritorno solo il limite massimo -> causa: miglioro prestazioni
		if (limit > de.limit_MAX):
			limit = de.limit_MAX

		if limit > len(cloud[de.history]):
			limit = len(cloud[de.history])
		
		mess = dict()
		print(f"LEGGO VALORI: sensori: {sensors}, limit: {limit}")
		for i, t in enumerate(cloud[de.history][-limit:]):
			mess = dict()
			#print(f'element on history: {t}')
			timestamps.append(t[de.timestamp])
			for s in t[de.values]:
				mess = dict()
				#print(f'element on history/values: {s}')
				# controllo che il sensore "aperto" sia richisto
				if ((s[de.sensorID] in sensors) or sensors == de.ALLsensors):
					#print(f"richiesto il sensore: {s[de.sensorID]}")
					if not str(s[de.sensorID]) in values.keys():
						values[str(s[de.sensorID])] = {de.t:[],
														de.h: [],
														de.d: [] }
					
					# aggiungo in automatico tutte le tipologia di misurazioni
					for tm in de.type_measurements:
						#print(f"tm: {tm}")
						#print(f" keys: {dict(s[de.value]).keys()}")
						if tm in s[de.value].keys():
							#print(f"tm: {tm} -> presente")
							# é presente una misurazione della temperatura, la aggiungo
							values[str(s[de.sensorID])][tm].append(s[de.value][tm])
						else:
							# se non ho misurazioni ritorno un None
							values[str(s[de.sensorID])][tm].append(None)
					#print(f"timestamps: {timestamps}, values: {values}")
				else:
					#print(f"sensore: {s[de.sensorID]} non richiesto")
					pass
			#print(f"\tmess: {mess}")
		print(f"timestamps: {timestamps}, values: {values}")
		return timestamps, values
