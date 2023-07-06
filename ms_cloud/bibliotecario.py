# stesso ruolo del burattinaio per il microservice_Catalogue

# il generale é colui che implementa i metodi per modificare/ ritornare valori richiesti dalle 2 parti (REST e MQTT 

import os
from time import time
from datetime import datetime
#import sys
#sys.path.insert(0, '/')
#from simulation.Cloud.read_cloud import ReadCloud as rc

import read_cloud as rc
import defines.defineExceptions as deExcept
import write_cloud as wc
import write_cloud_influxDB as wc_influxDB

import matplotlib.pyplot as plt
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import defines.defineJSONVariables as deJSONVar
de = deJSONVar.de()
import random

#import outputCommunications

import traceback

#import defineVariable as defineVariable
#de = defineVariable.de()
ex = deExcept.Exception()

import sys
#sys.path.append('D:\\POLITECNICO\\Magistrale\\A_IP\\project\\codice')
import ms_resource_catalog.read_catalogue as read_cat

class bibliotecario:
	def __init__(self):
		self.rd_cat = rc.ReadCloud(de.cloud_PATH_DEFAULT)
		self.wr_cat = wc.WriteCloud(de.cloud_PATH_DEFAULT)
		self.read_cat = read_cat.ReadInfoFromCatalogs(
                    de.cat_loc_1_PATH, de.cat_cannons_1_PATH, de.cat_sensors_1_PATH)
		
		# inizializzo client di influxDB
		#self.client_influx = InfluxDBClient(url=influxDB_settings[de.influxDB_URL], token=influxDB_settings[de.influxDB_token], org=influxDB_settings[de.influxDB_org])
		#write_api = self.client_influx.write_api(write_options=SYNCHRONOUS)
		
		#self.oc = outputCommunications.outputCommunications()
			
	def __init__(self, path: str, influxDB_settings):
		path_history = path + de.path_end_history
		path_locality = path + de.path_end_locality
		path_cannons = path + de.path_end_cannons
		path_sensors = path + de.path_end_sensors
		path_dev_cat = path + de.path_end_dev_cat
		
		self.rd_cat = rc.ReadCloud(path_history)
		self.wr_cat = wc.WriteCloud(path_history)

		self.read_cat = read_cat.ReadInfoFromCatalogs(
			path_locality, path_cannons, path_sensors, path_dev_cat)
		
		# old token influxDB_settings[de.influxDB_token]
		self.wr_cat_influxDB = wc_influxDB.WriteCloud_InfluxDB(
			url=influxDB_settings[de.influxDB_url], token=os.getenv(influxDB_settings[de.influxDB_token]), org=influxDB_settings[de.influxDB_org])
		

		#self.oc = outputCommunications.outputCommunications()

	#------------------------------------
	#			OTHER FUNCTION
	#------------------------------------
	def ControlChecksum(self, cks):
		#TODO IMPLEMENTARE controllo checksum
		return True

	def select(self, sensors, limit = de.limit_DEFAULT, day_referred = False ):
		try:
			sensors_int = [int(s) for s in sensors]
		except:
			return None
		# trasformazione stringa day_referred in qualcosa di sensato 
		print(f"richiesti sensori: {sensors_int}")
		t,v = self.rd_cat.select(sensors_int, limit, day_referred)
		return {de.timestamps: t, de.values: v}

	def addMeasurements(self, info):
		try:
			timestamp, values = info[de.timestamp],info[de.values]
			controParameter = wc.ControlInputParameter()
			# verifico che i dati inseriti siano del type richiesto
			#if not controParameter.Verify_some_inputs():
				#self.oc.PrintErrorMessage(ex.EXCEPTION_PARAMS_CATALOG_NOT_VALID)
				#return ex.EXCEPTION_PARAMS_CATALOG_NOT_VALID

			# verifico che l'id sia presente all'interno del catalogo
			values_presenti,values_assenti = controParameter.Verify_IDs_presence(values, self.read_cat.GetAllKitsIDs())
			print(f"indici presenti: {values_presenti}")
			# aggiorno le informazioni relative nel catalogo
			# aggiungo solo quelli presenti
			self.wr_cat.addMeasurement(timestamp, values_presenti)
			print("Cloud Modificato: Misurazioni aggiunte!")
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			#self.oc.PrintErrorMessage(ex.EXCEPTION_UPDATING_FAILED)
			return ex.EXCEPTION_UPDATING_FAILED

	# http://olgyay.polito.it:8090
	def addMeasurements_InfluxDB(self, fields, tags=[], name_point = de.kitID, bucket = de.bucket_Io3_raw_data, timestamp = datetime.utcnow()):
		try:
			# INPUT FORMAT data = [("co2",data["value"])], [("test_fit_3",data["tag"])]

			# aggiungere tutta la parte di controlli 

			'''nn = int(40 + random.randrange(-3, 3))
			nn2 = int(20 + random.randrange(-3, 3))
			self.wr_cat_influxDB.addMeasurement(
								bucket="Io3_Test1",\
				        		name_point="Io3_multiconfort", \
                                fields=[("co2", nn), ("temp", nn2), ("sens_fit", value)],
                            	tags=[("host_sens_fit", tag),("localityID", localityID)])'''
			
			self.wr_cat_influxDB.addMeasurement(
                            bucket=bucket,
                            name_point=name_point,
                            fields=fields,
                           	tags=tags, timestamp = datetime.now())
			
			print("Cloud Modificato: Misurazioni aggiunte!")

			a = 1
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			#self.oc.PrintErrorMessage(ex.EXCEPTION_UPDATING_FAILED)
			return ex.EXCEPTION_UPDATING_FAILED

	# http://olgyay.polito.it:8090	
	def Read_Measurements_InfluxDB(self, fields, tags=[], name_point = de.kitID, bucket = de.bucket_Io3_raw_data):
		try:
			print(f"Leggo le misurazioni - {bucket}:")
			# inizializzo struttura dati locale da ritornare a Dario
			data_retrieved = {}
			for field in fields:
				data_retrieved[field] = []

			#query = f'from(bucket: "{bucket}") |> range(start: -30d) |> filter(fn: (r) => r.host_sens_fit == "1")'
			query = f'from(bucket: "{bucket}") |> range(start: -15m) |> filter(fn: (r) => r._measurement == "kitID")'
			#query = f'from(bucket: "{bucket}") |> range(start: 2023-02-23T11:30:00Z, stop:2023-02-23T12:30:00Z ) |> filter(fn: (r) => r.host_sens_fit == "1")'
			tables = self.wr_cat_influxDB.client.query_api().query(query, org=self.wr_cat_influxDB.influxDB_org)
			
			for table in tables:

				print(f"table: {table}")
				print(f"Columns: ")
				for c in table.columns:
					print(f"\t{c.label}")
				for record in table.records:
					if record["_field"] in fields:
						data_retrieved[record["_field"]].append(record["_value"])
			print(data_retrieved)
			
			for k,v in data_retrieved.items():
				plt.plot(v)
				plt.ylabel(k)
				plt.show()
			a = 1
			return ex.DONE_CORRECT
		except Exception as exception:
			traceback.print_exc()
			#self.oc.PrintErrorMessage(ex.EXCEPTION_UPDATING_FAILED)
			return ex.EXCEPTION_UPDATING_FAILED
		
	def RetrieveDataToPopulateCards(self, kitID, fields=["a", "b", "c", "d", "e", "f", "g", "h", "i"]):
		bucket = de.bucket_Io3_raw_data

		#bucket = de.bucket_Io3_Test1
		data = {}
		for field in fields:
			data[field] = "ERROR"

		query = f'from(bucket: "{bucket}")  |> range(start: -30d)|> filter(fn: (r) => r.kitID == "{kitID}")|> last()'
		tables = self.wr_cat_influxDB.client.query_api().query(
			query, org=self.wr_cat_influxDB.influxDB_org)

		for table in tables:
			#print(f"table: {table}")
			#print(f"Columns: ")
			#for c in table.columns:
				#print(f"\t{c.label}")
			for record in table.records:
				if record["_field"] in fields:
					#data[record["_field"]].append(record["_value"])
					data[record["_field"]] = round(record["_value"],2)
		print(data)
		return data

	def GetStoricoData(self, kitID, fields=["a", "b", "c", "d", "e", "f", "g", "h", "i"], range_start= "-61s"):
		print(f"campii: {fields}")
		bucket = de.bucket_Io3_raw_data

		#bucket = de.bucket_Io3_Test1
		data = {}
		for field in fields:
			data[field] = []

		query = f'from(bucket: "{bucket}")  |> range(start: {range_start})|> filter(fn: (r) => r.kitID == "{kitID}")'
		tables = self.wr_cat_influxDB.client.query_api().query(
			query, org=self.wr_cat_influxDB.influxDB_org)

		for table in tables:
			#print(f"table: {table}")
			#print(f"Columns: ")
			#for c in table.columns:
				#print(f"\t{c.label}")
			for record in table.records:
				if record["_field"] in fields:
					data[record["_field"]].append([str(record["_time"]),round(record["_value"],2)])
		print(data)
		return data
		
