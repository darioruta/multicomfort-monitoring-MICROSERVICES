
from datetime import datetime
import json
# import json variable names under the variable de
import defines.defineJSONVariables as deJSONVar
de = deJSONVar.de()

import sys
import os
#sys.path.append('D:\\POLITECNICO\\Magistrale\\A_IP\\project\\codice')
sys.path.append(os.path.abspath(os.getcwd()))
import lib1 as lib1 
import json_utilization as ju

class ReadInfoFromCatalogs:
	def __init__(self, locality_catalog_path, cannons_catalog_path, kits_catalog_path, path_dev_cat):
		self.locality_catalog_path = locality_catalog_path
		self.cannons_catalog_path = cannons_catalog_path
		self.kits_catalog_path = kits_catalog_path
		self.dev_cat_path = path_dev_cat
  
	def GetInfoLocality(self, with_num_plessi = False):
		loc = ju.JsonMethods(fromJSONFile = self.locality_catalog_path).data
		# add info related num of slopes present
		if with_num_plessi:
			loc[de.info][de.num_plessi] = len([s[de.plessoID] for s in loc[de.plessi]])
		return loc[de.info]

	def GetPlessiStructure(self):
		loc = ju.JsonMethods(fromJSONFile=self.locality_catalog_path).data
		return [{de.plessoID: plesso[de.plessoID], de.aule: [aula[de.aulaID] for aula in plesso[de.aule]]} for plesso in loc[de.plessi]]

	def GetInfoCannonByCannonID(self, cannonID):
		cannons_cat = ju.JsonMethods(fromJSONFile = self.cannons_catalog_path).data
		cannon_info = [c for c in cannons_cat[de.cannons] if c[de.cannonID] == cannonID]
		#print(cannon_info)
		if len(cannon_info) > 1:
			print("ERRORE GRAVE (code: 0x01): cannonID non univoco -> ritorno il primo della lista")
		if len(cannon_info) == 0:
			print(f"cannonID: {cannonID} NOT PRESENT")
			return None
		# per ora ritorno tutto l'oggetto, magari servono meno informazioni
		return cannon_info[0]

	def GetInfoSensorBySensorID(self, sensorID):
		sensors_cat = ju.JsonMethods(fromJSONFile = self.kits_catalog_path).data
		sensor_info = [s for s in sensors_cat[de.kits] if s[de.kitID] == sensorID]
		if len(sensor_info) > 1:
			print("ERRORE GRAVE (code: 0x02): sensorID non univoco -> ritorno il primo della lista")
		if len(sensor_info) == 0:
			print(f"sensorID: {sensorID} NOT PRESENT")
			return None
		# per ora ritorno tutto l'oggetto, magari servono meno informazioni
		return sensor_info[0]
	def GetIfKitIsActive(self, kitID):
		cat = ju.JsonMethods(fromJSONFile= self.dev_cat_path)
		dev_cat = cat.data["dev_cat"]
		print(f"TIME NOW: {datetime.utcnow()}")
		# controllo che il kit sia presente dentro al dev_cat... potrebbe non essersi mai scritto
		if str(kitID) in dev_cat:
			kit_date = datetime.strptime(dev_cat[str(kitID)], '%Y-%m-%d %H:%M:%S.%f')
			print(kit_date)
			diff_sec = (datetime.utcnow() - kit_date).total_seconds()
			print(f"secondi passati dall'ultimo PING : {diff_sec}")
			if diff_sec < 60 * 10:   # < 10 minuti (si conta in secondi)
				# kit considerato attivo
				return True
		return False
	
	def GetAllKitsIDs(self):
		sensors_cat = ju.JsonMethods(fromJSONFile = self.kits_catalog_path).data
		return [s[de.kitID] for s in sensors_cat[de.kits]]

	
	def GetAllOnlineKitsIDs(self):
		all_kits = self.GetAllKitsIDs()
		kits = []
		# per ogni kit devo sapere dove é disposto
		for k in all_kits:
			# FORMAT pos = ["plessoID_1 ": [ "aula_1", "aula_2"]] 
			# ATTENZIONE -> io in realta prendo solo il primo plesso e la prima aula (associazione biunivoca!!)
			pos = self.SearchSensorID(k)
			
			kit = {}
			if len(pos) > 0:
				# significa che e posizionato
				kit[de.plessoName] = pos[0][de.plessoName]  # -> prendo il primo plesso della lista di posizione vere
				kit[de.plessoID] = pos[0][de.plessoID]
				kit[de.aulaName] = pos[0][de.aule][0] # -> prendo la prima aula della lista del primo plesso selezionato
			else:
				# se non é posizionato ritorno plesso: None, aula: None
				kit[de.plessoName] = None
				kit[de.aulaName] = None
				kit[de.plessoID] = None
			kit[de.kit_name] = self.GetInfoSensorBySensorID(k)[de.info_client][de.kit_name]
			kit["state"] = self.GetIfKitIsActive(k)
			kit[de.kitID] = k
			kits.append(kit)
			print(f"KIT {k}: ")
			print(kit)
		return kits

	def GetAllCannonsIDs(self):
		cannons_cat = ju.JsonMethods(fromJSONFile = self.cannons_catalog_path).data
		return [c[de.cannonID] for c in cannons_cat[de.cannons]]

	def SearchSensorID(self, sensorID):
		''' Search sensorID 
			ricerco in tutte le slope i settori dove compare il sensorID

			Returns
			-------
			una lista di plessi con all'interno i relativi aule dove compare il sensorID richiesto
		'''
		print("Search sensorID in all slopes and sectors")
		locality = ju.JsonMethods(fromJSONFile = self.locality_catalog_path).data
		# ogni slope puó avere piú settori dove compare lo stesso sensorID 
		# nel caso uno stesso sensore abilita diversi settori ( a noi non cambia nulla)
		slopes = list()
		#print(slopes_out)
		
		'''for sl in locality[de.plessi]:
			sectors = list()
			trovato = False
			#print(f"sl: {sl}")
			for se in sl[de.aule]:
				#print("\t" + str(se))
				for sensor in se[de.kits]:
					if sensor == sensorID:
						sectors.append(se[de.aulaID])
						# significa che almeno in un settore é stato trovato
						trovato = True
			#print(sectors)
			if trovato == True:
				slopes.append( { de.plessoID : sl[de.plessoID], 
						de.aule :  sectors
					}
					)
		print("\tOld Method" + str(slopes))'''
		#-------------------------------------------------------
		slopes_tmp = [{ de.plessoName : sl[de.plessoName], de.plessoID : sl[de.plessoID],
						de.aule :  [se[de.aulaName] for se in sl[de.aule] if sensorID in se[de.kits]] 
					} for sl in locality[de.plessi] ]
		slopes_new = list(filter(lambda el : el[de.aule] != [],slopes_tmp))
		# works if len([se[de.sectorID] for se in sl[de.sectors] if sensorID in se[de.sensors]])>0
		print("\tNew Method: "+ str(slopes_new))
		#-------------------------------------------------------
		#TODO se non vengono mai presentati errori eliminare metodo vecchio 
		#if slopes != slopes_new: raise NameError('New Method not equal to the old one modify_cat.SearchSensorID')
		
		return slopes_new

	def SearchCannonID(self, cannonID):
		''' Search sensorID 
			ricerco in tutte le slope i settori dove compare il cannonID

			Returns
			-------
			[
				{
					"slopeID" : 2,
					"sectors" : [
						1,
						2
					]
				},
				...
			]
			una lista di slopes con all'interno i relativi settori dove compare il cannonID richiesto
		'''
		print("Search cannonID in all slopes and sectors")
		locality = ju.JsonMethods(fromJSONFile = self.locality_catalog_path).data
		# ogni slope puó avere piú settori dove compare lo stesso sensorID 
		# nel caso uno stesso sensore abilita diversi settori ( a noi non cambia nulla)
		slopes = list()
		#print(slopes_out)
		for sl in locality[de.plessi]:
			sectors = list()
			trovato = False
			#print(f"sl: {sl}")
			for se in sl[de.aule]:
				#print("\t" + str(se))
				for cannon in se[de.cannons]:
					if cannon == cannonID:
						sectors.append(se[de.aulaID])
						# significa che almeno in un settore é stato trovato
						trovato = True
			#print(sectors)
			if trovato == True:
				slopes.append( { de.plessoID : sl[de.plessoID], 
						de.aule :  sectors
					}
					)
		print("\tOld Method" + str(slopes))
		#-------------------------------------------------------
		slopes_tmp = [{ de.plessoID : sl[de.plessoID], 
						de.aule :  [se[de.aulaID] for se in sl[de.aule] if cannonID in se[de.cannons]] 
					} for sl in locality[de.plessi] ]
		slopes_new = list(filter(lambda el : el[de.aule] != [],slopes_tmp))
		# works if len([se[de.sectorID] for se in sl[de.sectors] if cannonID in se[de.cannons]])>0
		print("\tNew Method: "+ str(slopes_new))
		#-------------------------------------------------------
		#TODO se non vengono mai presentati errori eliminare metodo vecchio 
		if slopes != slopes_new: raise NameError('New Method not equal to the old one modify_cat.SearchCannonID')
		
		return slopes
	def GetAllPlessiID(self):
		locality = ju.JsonMethods(fromJSONFile = self.locality_catalog_path).data
		#TODO verificare se funziona
		return [s[de.plessoID] for s in locality[de.plessi]]
	def GetAllAuleIDinPlesso(self, plessoID):
		locality = ju.JsonMethods(fromJSONFile = self.locality_catalog_path).data
		return [se[de.aulaID] for sl in locality[de.plessi] for se in sl[de.aule] if sl[de.plessoID] == plessoID]
	
	def GetAllCannonsIDsInSectorIDandSlopeID(self, slopeID, sectorID):
		locality = ju.JsonMethods(fromJSONFile=self.locality_catalog_path).data
		slopes = [s for s in locality[de.plessi] if s[de.plessoID] == slopeID]
		if len(slopes) == 0:
			print(f"slopeID: {slopeID} NOT PRESENT")
		else:
			sectors = [s for s in slopes[0][de.aule] if s[de.aulaID] == sectorID]
			if len(sectors) == 0:
				print(f"sectorID: {sectorID} NOT PRESENT")
				return []
			else:
				return sectors[0][de.cannons]

	def GetAllSensorsIDsInSectorIDandSlopeID(self, slopeID, sectorID):
		locality = ju.JsonMethods(fromJSONFile=self.locality_catalog_path).data
		slopes = [s for s in locality[de.plessi] if s[de.plessoID] == slopeID]
		if len(slopes) == 0:
			print(f"slopeID: {slopeID} NOT PRESENT")
		else:
			sectors = [s for s in slopes[0][de.aule] if s[de.aulaID] == sectorID]
			if len(sectors) == 0:
				print(f"sectorID: {sectorID} NOT PRESENT")
				return []
			else:
				return sectors[0][de.kits]

	def GetAllCannonCatalogue(self):
		return ju.JsonMethods(fromJSONFile=self.cannons_catalog_path).data
	def GetAllKitCatalogue(self):
		return ju.JsonMethods(fromJSONFile=self.kits_catalog_path).data
	def GetAllLocalityCatalogue(self):
		return ju.JsonMethods(fromJSONFile=self.locality_catalog_path).data


