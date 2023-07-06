# import json variable names under the variable de
import defines.defineExceptions as deExcept
import defines.defineJSONVariables as deJSONVar
de = deJSONVar.de()

# import json variable names under the variable de
import defines.defineURIMicroservices as deMicroServices
deMS = deMicroServices.de_microservices()

import defines.defineExceptions as deExcept
ex = deExcept.Exception()

import modiy_catalog as mc
import read_catalogue as rc
import outputCommunications


import traceback 

# rimuovere alla fine
import json_utilization as ju
# fine rimossione

class burattinaio: 
	def __init__(self):
		self.read_cat = rc.ReadInfoFromCatalogs(de.cat_loc_1_PATH, de.cat_cannons_1_PATH, de.cat_sensors_1_PATH) 
		self.mod_cat = mc.ModifyCatalog(de.cat_loc_1_PATH, de.cat_cannons_1_PATH, de.cat_sensors_1_PATH )

		self.oc = outputCommunications.outputCommunications()

	def __init__(self, path ):
		path_locality = path + de.path_end_locality
		path_cannons = path + de.path_end_cannons
		path_sensors = path + de.path_end_sensors
		path_dev_cat = path + de.path_end_dev_cat
		self.read_cat = rc.ReadInfoFromCatalogs(path_locality, path_cannons, path_sensors, path_dev_cat) 
		self.mod_cat = mc.ModifyCatalog(path_locality, path_cannons, path_sensors) 

		self.path_base = path
		self.oc = outputCommunications.outputCommunications()
	#------------------------------------
	#			GET OBJECT
	#------------------------------------
	# NOT USED
	def GetAllCannonCatalogue(self):
		try:
			l = self.read_cat.GetAllCannonCatalogue()
			return l
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.return_error_message(ex.EXCEPTION_READ_FAILED))
			return ex.return_error_message(ex.EXCEPTION_READ_FAILED)
	# NOT USED END

	def GetAllKitCatalogue(self):
		try:
			l = self.read_cat.GetAllKitCatalogue()
			return l
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.return_error_message(ex.EXCEPTION_READ_FAILED))
			return ex.return_error_message(ex.EXCEPTION_READ_FAILED)

	def GetAllLocalityCatalogue(self):
		try:
			l = self.read_cat.GetAllLocalityCatalogue()
			return l
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.return_error_message(ex.EXCEPTION_READ_FAILED))
			return ex.return_error_message(ex.EXCEPTION_READ_FAILED)

	def GetAllPlessiID(self):
		try: 
			l = self.read_cat.GetAllPlessiID()
			return {"IDs": l}
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.return_error_message(ex.EXCEPTION_READ_FAILED))
			return ex.return_error_message(ex.EXCEPTION_READ_FAILED)

	def GetPlessiStructure(self):
		try:
			l = self.read_cat.GetPlessiStructure()
			return {"plessiList": l}
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.return_error_message(ex.EXCEPTION_READ_FAILED))
			return ex.return_error_message(ex.EXCEPTION_READ_FAILED)

	def GetAllAuleIDinPlessoID(self, plessoID):
		try:
			if (not plessoID in self.read_cat.GetAllPlessiID()):
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				return ex.EXCEPTION_OBJECT_NOT_PRESENT
			l = self.read_cat.GetAllAuleIDinPlesso(plessoID)
			return {"IDs": l}
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.return_error_message(ex.EXCEPTION_READ_FAILED))
			return ex.return_error_message(ex.EXCEPTION_READ_FAILED)
	def GetAllCannonsIDs(self):
		try:
			l = self.read_cat.GetAllCannonsIDs()
			return {"CannonsIDs": l}
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.return_error_message(ex.EXCEPTION_READ_FAILED))
			return ex.return_error_message(ex.EXCEPTION_READ_FAILED)
	
	def GetAllCannonsIDsInSectorIDandSlopeID(self, slopeID, sectorID):
		try:
			controParameter = mc.ControlInputParameter()
			# verifico che i dati inseriti siano del type richiesto
			#if not controParameter.VerifyCannonInputs(info[de.type], info[de.mode], info[de.state], info[de.info][de.prog_on], info[de.info][de.prog_off], info[de.info][de.auto_threshold]):
			#TODO cambiare metodo di controllo
			if not controParameter.VerifySlopeIDSectorIDInputs(slopeID, sectorID):
				self.oc.PrintErrorMessage(ex.EXCEPTION_PARAMS_CATALOG_NOT_VALID)
				return ex.EXCEPTION_PARAMS_CATALOG_NOT_VALID
			slopeID = int(slopeID)
			sectorID =  int(sectorID)
			if (not slopeID in self.read_cat.GetAllPlessiID()):
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				print(f"slopeID: {slopeID} non presente")
				return ex.EXCEPTION_OBJECT_NOT_PRESENT
			if (not sectorID in self.read_cat.GetAllAuleIDinPlesso(slopeID)):
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				print(f"sectorID: {sectorID} non presente")
				return ex.EXCEPTION_OBJECT_NOT_PRESENT
			c = self.read_cat.GetAllCannonsIDsInSectorIDandSlopeID(slopeID, sectorID)
			return {"CannonsIDs": c}
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.return_error_message(ex.EXCEPTION_READ_FAILED))
			return ex.return_error_message(ex.EXCEPTION_READ_FAILED)

	def GetAllSensorsIDsInSectorIDandSlopeID(self, slopeID, sectorID):
		try:
			controParameter = mc.ControlInputParameter()
			# verifico che i dati inseriti siano del type richiesto
			#if not controParameter.VerifyCannonInputs(info[de.type], info[de.mode], info[de.state], info[de.info][de.prog_on], info[de.info][de.prog_off], info[de.info][de.auto_threshold]):
			#TODO cambiare metodo di controllo
			if not controParameter.VerifySlopeIDSectorIDInputs(slopeID, sectorID):
				self.oc.PrintErrorMessage(ex.EXCEPTION_PARAMS_CATALOG_NOT_VALID)
				return ex.EXCEPTION_PARAMS_CATALOG_NOT_VALID

			slopeID = int(slopeID)
			sectorID = int(sectorID)
			if (not slopeID in self.read_cat.GetAllPlessiID()):
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				return ex.EXCEPTION_OBJECT_NOT_PRESENT
			if (not sectorID in self.read_cat.GetAllAuleIDinPlesso(slopeID)):
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				return ex.EXCEPTION_OBJECT_NOT_PRESENT
			s = self.read_cat.GetAllSensorsIDsInSectorIDandSlopeID(slopeID, sectorID)
			return {"SensorsIDs": s}
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.return_error_message(ex.EXCEPTION_READ_FAILED))
			return ex.return_error_message(ex.EXCEPTION_READ_FAILED)

	def GetAllKitsIDs(self):
		try:
			l = self.read_cat.GetAllKitsIDs()
			return {"KitsIDs": l}
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.return_error_message(ex.EXCEPTION_READ_FAILED))
			return ex.return_error_message(ex.EXCEPTION_READ_FAILED)
		
	def GetAllOnlineKitsIDs(self):
		l = self.read_cat.GetAllOnlineKitsIDs()
		try:
			l = self.read_cat.GetAllOnlineKitsIDs()
			return {"KitsIDs": l}
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.return_error_message(ex.EXCEPTION_READ_FAILED))
			return ex.return_error_message(ex.EXCEPTION_READ_FAILED)
	def GetInfoCannonByCannonID(self, cannonID):
		try:
			l = self.read_cat.GetInfoCannonByCannonID(cannonID)
			pos = self.read_cat.SearchCannonID(cannonID)
			return {"CannonInfo": l, "Position": pos}
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.return_error_message(ex.EXCEPTION_READ_FAILED))
			return ex.return_error_message(ex.EXCEPTION_READ_FAILED)
	def GetInfoSensorBySensorID(self, sensorID):
		try:
			l = self.read_cat.GetInfoSensorBySensorID(sensorID)
			pos = self.read_cat.SearchCannonID(sensorID)
			return {"SensorInfo": l, "Position": pos}
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.return_error_message(ex.EXCEPTION_READ_FAILED))
			return ex.return_error_message(ex.EXCEPTION_READ_FAILED)

	def GetInfoLocality(self, num_plessi = False):
		try:
			l = self.read_cat.GetInfoLocality(num_plessi)
			return l
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.return_error_message(ex.EXCEPTION_READ_FAILED))
			return ex.return_error_message(ex.EXCEPTION_READ_FAILED)
			
	def AddCannonToSlopeSector(self, slopeID, sectorID, cannonID):
		try:
			if not cannonID in self.read_cat.GetAllCannonsIDs():
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				return ex.EXCEPTION_OBJECT_NOT_PRESENT
			print(f"cannonID {cannonID} PRESENTE")
			if (not slopeID in self.read_cat.GetAllPlessiID()) or \
					(not sectorID in self.read_cat.GetAllAuleIDinPlesso(slopeID)):
				# in caso si volesse togliere l'associazione -> slopeID = 0, sectorID = 0
				if slopeID == 0 and sectorID == 0:
					self.mod_cat.RemoveCannonByCannonIDFromAllSlopes(cannonID)
					return ex.DONE_CORRECT
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				return ex.EXCEPTION_OBJECT_NOT_PRESENT
			self.mod_cat.RemoveCannonByCannonIDFromAllSlopes(cannonID)
			self.mod_cat.AddCannonToSlopeSector(slopeID, sectorID, cannonID)
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.EXCEPTION_UPDATING_FAILED)
			return ex.EXCEPTION_UPDATING_FAILED

	def AddKitToPlessoAula(self, plessoID, aulaID, kitID):
		try:
			if not kitID in self.read_cat.GetAllKitsIDs():
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				return ex.EXCEPTION_OBJECT_NOT_PRESENT
			print(f"sensorID {kitID} PRESENTE")
			if (not plessoID in self.read_cat.GetAllPlessiID()) or \
					(not aulaID in self.read_cat.GetAllAuleIDinPlesso(plessoID)):
				# in caso si volesse togliere l'associazione -> slopeID = 0, sectorID = 0
				if plessoID == 0 and aulaID == 0:
					self.mod_cat.RemoveKitByKitIDFromAllPlessi(kitID)
					return ex.DONE_CORRECT
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				return ex.EXCEPTION_OBJECT_NOT_PRESENT
			self.mod_cat.RemoveKitByKitIDFromAllPlessi(kitID)
			self.mod_cat.AddSensorToSlopeSector(plessoID, aulaID, kitID)
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.EXCEPTION_UPDATING_FAILED)
			return ex.EXCEPTION_UPDATING_FAILED
		
	def Update_Ping_Device_Catalog(self, dev_name, t):
		try:
			cat = ju.JsonMethods(fromJSONFile= self.path_base + "/dev_cat.json")
			dev_cat = cat.data
			dev_cat["dev_cat"][dev_name] = t
			cat.dumpsJson()

			print("")

			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.EXCEPTION_UPDATING_FAILED)
			return ex.EXCEPTION_UPDATING_FAILED


	def SetInfoCannonByCannonID(self, info):
		try:
			controParameter = mc.ControlInputParameter()
			# verifico che i dati inseriti siano del type richiesto
			#if not controParameter.VerifyCannonInputs(info[de.type], info[de.mode], info[de.state], info[de.info][de.prog_on], info[de.info][de.prog_off], info[de.info][de.auto_threshold]):
			#TODO cambiare metodo di controllo
			if not controParameter.VerifyCannonInputs("type", "model", "state" ):
				self.oc.PrintErrorMessage(ex.EXCEPTION_PARAMS_CATALOG_NOT_VALID)
				return ex.EXCEPTION_PARAMS_CATALOG_NOT_VALID
			# verifico che l'id sia presente all'interno del catalogo
			if not info[de.cannonID] in self.read_cat.GetAllCannonsIDs():
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				return ex.EXCEPTION_OBJECT_NOT_PRESENT
			# aggiorno le informazioni relative nel catalogo
			self.mod_cat.SetCannonInfo(info)
			print("Catalogo modificato")
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.EXCEPTION_UPDATING_FAILED)
			return ex.EXCEPTION_UPDATING_FAILED
	def SetInfoKitByKitID(self, info):
		try:	
			controParameter = mc.ControlInputParameter()
			# verifico che i dati inseriti siano del type richiesto
			if not controParameter.VerifySensorInputs():
				self.oc.PrintErrorMessage(ex.EXCEPTION_PARAMS_CATALOG_NOT_VALID)
				return ex.EXCEPTION_PARAMS_CATALOG_NOT_VALID
				
			# verifico che l'id sia presente all'interno del catalogo
			if not info[de.kitID] in self.read_cat.GetAllKitsIDs():
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				return ex.EXCEPTION_OBJECT_NOT_PRESENT
			# aggiorno le informazioni relative nel catalogo
			self.mod_cat.SetKitInfo(info)
			print("Catalogo modificato -> SetKitInfo")
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.EXCEPTION_UPDATING_FAILED)
			return ex.EXCEPTION_UPDATING_FAILED
	#------------------------------------
	#			DELETE OBJECT
	#------------------------------------
	def DropCannonByCannonID(self,cannonID):
		try: 
			if not cannonID in self.read_cat.GetAllCannonsIDs():
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				return  ex.EXCEPTION_OBJECT_NOT_PRESENT
			self.mod_cat.RemoveCannonByCannonIDFromAllSlopes(cannonID)
			self.mod_cat.DeleteCannonByCannonID(cannonID)
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.EXCEPTION_DELETE_FAILED)
			return ex.EXCEPTION_DELETE_FAILED
	def DropKitByKitID(self,kitID):
		try:
			if not kitID in self.read_cat.GetAllKitsIDs():
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				return ex.EXCEPTION_OBJECT_NOT_PRESENT
			self.mod_cat.RemoveKitByKitIDFromAllPlessi(kitID)
			self.mod_cat.DeleteKitByKitID(kitID)
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.EXCEPTION_DELETE_FAILED)
			return ex.EXCEPTION_DELETE_FAILED

	def DropPlessoByPlessoID(self,slopeID):
		try:
			if not slopeID in self.read_cat.GetAllPlessiID():
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				return ex.EXCEPTION_OBJECT_NOT_PRESENT
			err = self.mod_cat.DeleteSlopeBySlopeID(slopeID)
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.EXCEPTION_DELETE_FAILED)
			return ex.EXCEPTION_DELETE_FAILED

	def DropAulaByAulaIDAndPlessoID(self, slopeID, sectorID):	
		try:
			if (not slopeID in self.read_cat.GetAllPlessiID()) or \
					(not sectorID in self.read_cat.GetAllAuleIDinPlesso(slopeID)):
				self.oc.PrintErrorMessage(ex.EXCEPTION_OBJECT_NOT_PRESENT)
				return ex.EXCEPTION_OBJECT_NOT_PRESENT
			err = self.mod_cat.DeleteSectorBySlopeIDAndSectorID(slopeID, sectorID)
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.EXCEPTION_DELETE_FAILED)
			return ex.EXCEPTION_DELETE_FAILED
	#------------------------------------
	#			ADD NEW OBJECT
	#------------------------------------
	def AddNewCannon(self):
		try: 
			newCannonID = self.GetaNewCannonID()
			cannonObj = mc.DefaultCatalogues().GetCannonDefault(newCannonID)
			self.mod_cat.AddNewCannon(cannonObj)
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.EXCEPTION_ADD_OBJECT_FAILED)
			return ex.return_error_message(ex.EXCEPTION_ADD_OBJECT_FAILED)
	def AddNewSensor(self, info = {}):
		try:
			newSensorID = self.GetaNewSensorID()
			sensorObj = mc.DefaultCatalogues().GetkitDefault(newSensorID)
			self.mod_cat.AddNewSensor(sensorObj)

			if info != {}:
				info[de.kitID] = newSensorID
				return self.SetInfoKitByKitID(info)
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.EXCEPTION_ADD_OBJECT_FAILED)
			return ex.return_error_message(ex.EXCEPTION_ADD_OBJECT_FAILED)

	def AddNewSlope(self):
		try: 
			newSlopeID = self.GetaNewSlopeID()
			slopeObj = mc.DefaultCatalogues().GetSlopeDefaultByNewID(newSlopeID)
			self.mod_cat.AddSlopeToLocality(slopeObj)
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.EXCEPTION_ADD_OBJECT_FAILED)
			return ex.return_error_message(ex.EXCEPTION_ADD_OBJECT_FAILED)
	def AddNewSectorToSlope(self, slopeID):
		try:
			if not slopeID in self.read_cat.GetAllPlessiID():
				return False
			newSectorID = self.GetaNewSectorIDforCertainSlope(slopeID)
			sectorObj = mc.DefaultCatalogues().GetSectorDefaultByNewID(newSectorID)
			self.mod_cat.AddSectorToSlope(slopeID, sectorObj)
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			self.oc.PrintErrorMessage(ex.EXCEPTION_ADD_OBJECT_FAILED)
			return ex.return_error_message(ex.EXCEPTION_ADD_OBJECT_FAILED)
	#------------------------------------
	#			OTHER FUNCTION
	#------------------------------------
	def ControlChecksum(self, cks):
		#TODO IMPLEMENTARE controllo checksum
		return True


	def GetaNewSlopeID(self):
		slopeID_present = self.read_cat.GetAllPlessiID()
		if len(slopeID_present) == 0:
			return de.ID_default
		new_id = 1 + max(slopeID_present)
		trovato = False
		#TODO qua l'unico problema si ritrova se abbiamo N = max(var int)
		# e quindi non abbiamo piú numeri inutilizzabili -> condizione impossibile nella realtá
		while trovato == False:
			if new_id in slopeID_present:
				++ new_id
			else:
				trovato = True
		# new_id is unique
		return new_id

	def GetaNewSectorIDforCertainSlope(self, slopeID):
		sectorID_present = self.read_cat.GetAllAuleIDinPlesso(slopeID)
		if len(sectorID_present) == 0:
			return de.ID_default
		new_id = 1 + max(sectorID_present)
		trovato = False
		#TODO qua l'unico problema si ritrova se abbiamo N = max(var int)
		# e quindi non abbiamo piú numeri inutilizzabili -> condizione impossibile nella realtá
		while trovato == False:
			if new_id in sectorID_present:
				++ new_id
			else:
				trovato = True
		# new_id is unique
		return new_id
	def GetaNewSensorID(self):
		sensorID_present = self.read_cat.GetAllKitsIDs()
		if len(sensorID_present) == 0:
			return de.ID_default
		new_id = 1 + max(sensorID_present)
		trovato = False
		#TODO qua l'unico problema si ritrova se abbiamo N = max(var int)
		# e quindi non abbiamo piú numeri inutilizzabili -> condizione impossibile nella realtá
		while trovato == False:
			if new_id in sensorID_present:
				++new_id
			else:
				trovato = True
		# new_id is unique
		return new_id

	def GetaNewCannonID(self):
		cannonID_present = self.read_cat.GetAllCannonsIDs()
		if len(cannonID_present) == 0:
			return de.ID_default
		new_id = 1 + max(cannonID_present)
		trovato = False
		#TODO qua l'unico problema si ritrova se abbiamo N = max(var int)
		# e quindi non abbiamo piú numeri inutilizzabili -> condizione impossibile nella realtá
		while trovato == False:
			if new_id in cannonID_present:
				++ new_id
			else:
				trovato = True
		# new_id is unique
		return new_id

'''
# NON utilizzato!!!!!
class GetNewIDs:
	def __init__(self, file_catalogue):
		# potrei non salvarla come self.cat_json per guadagnare spazio in memoria
		self.SiC = SearchInCatalog(file_catalogue = file_catalogue) 
	def GetaNewSlopeID(self):
		raise Exception("NOT implemented")
	def GetaNewSectorIDforCertainSlope(self, slopeID):
		raise Exception("NOT implemented")

		'''