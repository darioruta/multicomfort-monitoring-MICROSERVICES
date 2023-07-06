import lib.json_utilization as ju
import lib.lib1 as lib1

import read_catalogue as rc
# import json variable names under the variable de
import defines.defineJSONVariables as deJSONVar
de = deJSONVar.de()

import defines.defineExceptions as deExcept
ex = deExcept.Exception()




	
class ControlInputParameter:
	def VerifyLocalityInfo(self,locName, mslm):
		if lib1.check_user_input(locName,de.FORMAT_STRING) and \
				lib1.check_user_input(mslm, de.FORMAT_INT):
			return True
		else:
			print(f"input non corretti! \n \
				\t {de.localityName} -> STRING \n \
				\t {de.mslm} -> INT \n ")
			return False
	def VerifySlopeIDSectorIDInputs(self, slopeID, sectorID):
		if lib1.check_user_input(slopeID, de.FORMAT_INT) and \
                        lib1.check_user_input(sectorID, de.FORMAT_INT):
			return True
		else:
			print(f"input non corretti! \n \
				\t {de.plessoID} -> INT \n \
				\t {de.aulaID} -> INT \n ")
			return False
	def VerifyCannonInputs(self,t,m,s,p_on = "",p_off = "", a_t = -1):
		if lib1.check_user_input(t,de.FORMAT_STRING) and \
			lib1.check_user_input(m,de.FORMAT_STRING) and \
				lib1.check_user_input(s,de.FORMAT_STRING) and \
					lib1.check_user_input(p_on,de.FORMAT_STRING) and \
						lib1.check_user_input(p_off,de.FORMAT_STRING) and \
							lib1.check_user_input(a_t, de.FORMAT_INT):
			print("NOT ALREARY IMPLEMENTED ---> DA FARE #TODO ")
			print("PER ORA VADO AVANTI")
			return True
		else:
			#TODO non so se servono prog on e prog off
			print(f"input non corretti! \n \
				\t {de.type} -> STRING \n \
				\t {de.mode} -> STRING \n \
				\t {de.state} -> STRING \n \
				\t {de.prog_on} -> STRING \n \
				\t {de.prog_off} -> STRING \n \
					")
			return False
	def VerifySensorInputs(self):
		#TODO implementare come nei cannoni
		print("NOT ALREARY IMPLEMENTED ---> DA FARE #TODO ")
		print("PER ORA VADO AVANTI")
		return True

	
				
class ManageWorld:
	def __init__(self,file_world_path):
		self.path = file_world_path
	def GetPathByLocalityID(self,localityID):
		w = ju.JsonMethods(fromJSONFile = self.path).data
		list_locID = [l[de.localityID] for l in w[de.localities]]
		if localityID not in list_locID:
			print("localityID requested NOT present")
			return False
		else:
			return w[de.localities][list_locID.index(localityID)][de.path]

#classe dedicata a modificare il catalogo online
class ModifyCatalog:
	def __init__(self,file_catalogue,cannons_file_path, sensors_file_path = de.cat_sensors_1_PATH):
		self.catalogue_path = file_catalogue
		self.cannons_catalogue_path = cannons_file_path
		self.sensors_catalogue_path = sensors_file_path
	def AddAcquisitionToSensor(self,  sensor, measurement):
		sensor[de.data].append(measurement)
		return sensor
	def AddSensorToSector(self, SlopeID ,sectorID, sensorID):
		locality = ju.JsonMethods(fromJSONFile = self.catalogue_path).data
		indSlope = [slID[de.plessoID] for slID in locality[de.plessi]].index(SlopeID)
		indSector = [secID[de.aulaID] for secID in locality[de.plessi][indSlope][de.aule]].index(sectorID)
		locality[de.plessi][indSlope][de.aule][indSector].append(sensorID)
		print(f"\t Aggiunto a  a slopeID: {SlopeID}, sectorID: {sectorID} il sensorID: {sensorID}")

	def AddSectorToSlope ( self, slopeID, sector):
		cat = ju.JsonMethods(fromJSONFile=self.catalogue_path)
		locality = cat.data
		ind = [slID[de.plessoID] for slID in locality[de.plessi]].index(slopeID)
		locality[de.plessi][ind][de.aule].append(sector)
		cat.dumpsJson()
		print(f"\t Aggiunto sectorID: {sector[de.aulaID]} a slopeID: {slopeID}")

	def AddSlopeToLocality ( self, slope):
		cat = ju.JsonMethods(fromJSONFile = self.catalogue_path)
		locality = cat.data
		locality[de.plessi].append(slope)
		cat.dumpsJson()
		print(f"\t Aggiunta Slope a Locality: {locality[de.localityID]}") 
  
	def AddNewCannon(self,cannon):
		cat_c = ju.JsonMethods(fromJSONFile = self.cannons_catalogue_path)
		cat_c.data[de.cannons].append(cannon)
		cat_c.dumpsJson()
		print(f"\t Aggiunto nuovo Cannone -> ID: {cannon[de.cannonID]}")	

	def AddNewSensor(self, sensor):
		cat_s = ju.JsonMethods(fromJSONFile=self.sensors_catalogue_path)
		cat_s.data[de.kits].append(sensor)
		cat_s.dumpsJson()
		print(f"\t Aggiunto nuovo Sensore -> ID: {sensor[de.kitID]}")

	def AddCannonToSlopeSector(self, slopeID, sectorID, cannonID):
		cat = ju.JsonMethods(fromJSONFile=self.catalogue_path)
		locality = cat.data
		indexSlope = [slope[de.plessoID] for slope in locality[de.plessi]].index(slopeID)
		indexSector = [sector[de.aulaID] for sector in locality[de.plessi][indexSlope][de.aule]].index(sectorID)
		locality[de.plessi][indexSlope][de.aule][indexSector][de.cannons].append(cannonID)
		cat.dumpsJson()
		print(f"\t Aggiunto Cannone {cannonID} -> into: Slope: {slopeID}, Sector: {sectorID}")

	def AddSensorToSlopeSector(self, slopeID, sectorID, sensorID):
		cat = ju.JsonMethods(fromJSONFile=self.catalogue_path)
		locality = cat.data
		indexSlope = [slope[de.plessoID] for slope in locality[de.plessi]].index(slopeID)
		indexSector = [sector[de.aulaID] for sector in locality[de.plessi][indexSlope][de.aule]].index(sectorID)
		locality[de.plessi][indexSlope][de.aule][indexSector][de.kits].append(sensorID)
		cat.dumpsJson()
		print(f"\t Aggiunto Sensore {sensorID} -> into: Slope: {slopeID}, Sector: {sectorID}")

	def DeleteSlopeBySlopeID(self,slopeID):
		cat = ju.JsonMethods(fromJSONFile = self.catalogue_path)
		locality = cat.data
		index = [slope[de.plessoID] for slope in locality[de.plessi]].index(slopeID)
		del locality[de.plessi][index]
		cat.dumpsJson()
		print(f"\t Eliminata Slope {slopeID} nella Locality: {locality[de.localityID]}")

	def DeleteSectorBySlopeIDAndSectorID(self,slopeID, sectorID):
		cat = ju.JsonMethods(fromJSONFile = self.catalogue_path)
		locality = cat.data
		index_slope = [slope[de.plessoID] for slope in locality[de.plessi]].index(slopeID)
		index_sector = [ sec[de.aulaID] for sec in locality[de.plessi][index_slope][de.aule]].index(sectorID) 
		del locality[de.plessi][index_slope][de.aule][index_sector]
		cat.dumpsJson()
		print(f"\t Eliminato Sector {sectorID} da Slope {slopeID} nella Locality: {locality[de.localityID]}")

	def DeleteCannonByCannonIDFromCannonCatalog(self, cannonID):
		cat_c = ju.JsonMethods(fromJSONFile=self.cannons_catalogue_path)
		cannons_cat = cat_c.data
		index_cannon = [cann[de.cannonID] for cann in cannons_cat[de.cannons]].index(cannonID)
		del cannons_cat[de.cannons][index_cannon]
		cat_c.dumpsJson()
		print(f"\t Eliminato Cannon {cannonID} dalla cannonCatalog: {cannons_cat[de.cannons_catalog_ID]}")

	def RemoveCannonByCannonIDFromAllSlopes(self, cannonID):
		cat_l = ju.JsonMethods(fromJSONFile=self.catalogue_path)
		locality = cat_l.data
		for slope in locality[de.plessi]:
			for sector in slope[de.aule]:
				if cannonID in sector[de.cannons]:
					sector[de.cannons].remove(cannonID)
		cat_l.dumpsJson()
		print(f"\t Eliminato Cannon {cannonID} dalla Locality: {locality[de.info][de.localityName]}")

	def DeleteKitByKitID(self, sensorID):
		cat_s = ju.JsonMethods(fromJSONFile=self.cannons_catalogue_path)
		sensors_cat = cat_s.data
		index_sensor = [sen[de.kitID] for sen in sensors_cat[de.kits]].index(sensorID)
		del sensors_cat[de.kits][index_sensor]
		cat_s.dumpsJson()
		print(f"\t Eliminato Sensor {sensorID} dalla sensorCatalog: {sensors_cat[de.kits_catalog_ID]}")

	def RemoveKitByKitIDFromAllPlessi(self, sensorID):
		cat_l = ju.JsonMethods(fromJSONFile=self.catalogue_path)
		locality = cat_l.data
		for slope in locality[de.plessi]:
			for sector in slope[de.aule]:
				if sensorID in sector[de.kits]:
					sector[de.kits].remove(sensorID)
		cat_l.dumpsJson()
		print(f"\t Eliminato Sensor {sensorID} dalla Locality: {locality[de.info][de.localityName]}")
	
	def AddMeasurementToDataRecorded(self, meas, slopes_out, data_rec):
		# meas = measurements to add to data_rec
		# must have this format
		'''{
				"sensorID": 1,
				"data":[
					{
						"timestamp": "",
						"temperature": [],
						"humidity": [],
						"deepsensor": []
					}
				]
			}'''
		# slopes_out = lista di piste e relativi sensori a cui é legata la measurements
		# data_rec é il database dove ci sono tutte le misurazioni passate ) si deve aggiungere a questo la nuova misura
		for dr in data_rec[de.plessi]:
			for s_out in slopes_out: 
				if dr[de.plessoID] == s_out[de.plessoID]:
					for sec in dr[de.aule]:
						if sec[de.aulaID] in s_out[de.aule]:
							for sen in sec[de.kits]:
								if sen[de.kitID] == meas[de.kitID]:
									self.AddAcquisitionToSensor(sen,meas[de.data])
	def SetCannonInfo(self, cannon, new_cannon = False):
		cat_c = ju.JsonMethods(fromJSONFile = self.cannons_catalogue_path)
		# get cannon Object looking at cannonID
		if new_cannon:
			cat_c.data[de.cannons].append(DefaultCatalogues().GetCannonDefault())
			cannon_index = len(cat_c.data[de.cannons]) - 1
		else:
			cannon_index = [c[de.cannonID] for c in cat_c.data[de.cannons]].index(cannon[de.cannonID])
		for k in list(cat_c.data[de.cannons][cannon_index].keys()):
			if k in list(cannon.keys()):
				cat_c.data[de.cannons][cannon_index][k] = cannon[k]
		cat_c.dumpsJson()
	def SetKitInfo(self, sensor, new_sensor = False):
		cat_s = ju.JsonMethods(fromJSONFile = self.sensors_catalogue_path)
		# get sensor Object looking at sensorID 
		if new_sensor:
			cat_s.data[de.kits].append(DefaultCatalogues().GetkitDefault())
			sensor_index = len(cat_s.data[de.kits]) - 1
		else:
			sensor_index = [s[de.kitID] for s in cat_s.data[de.kits]].index(sensor[de.kitID])
		for k in list(cat_s.data[de.kits][sensor_index].keys()):
			if k in list(sensor.keys()):
				cat_s.data[de.kits][sensor_index][k] = sensor[k]
		cat_s.dumpsJson()

class DefaultCatalogues():
	def __init__(self):
		pass
	def GetkitDefault(self, kitID):
		kit = {
			de.kitID: kitID,
			de.kit_MAC: "",
			de.info_client:{
				de.kit_name:"",
				de.kit_model: "",
				de.date_assembly: ""
			}
		}
		return kit
	def GetCannonDefault(self, cannonID):
		cannon = {
			de.cannonID: cannonID,
			de.type: "",
			de.mode : "",
			de.state: "",
			de.info:{
				de.prog_on: "",
				de.prog_off: "",
				de.auto_threshold : -1
			},
			de.info_client:{
				de.cannon_name:"",
				de.cannon_model:"",
				de.water_volume: -1
			}
		}
		return cannon
	def GetSlopeDefaultByNewID(self,plessoID):
		plesso = {
			de.plessoID : plessoID,
			de.aule : []
		}
		return plesso
	def GetSectorDefaultByNewID(self, sectorID):
		sector = {
				de.aulaID: sectorID,
				de.kits: [],
				de.cannons: []
			}
		return sector
							
