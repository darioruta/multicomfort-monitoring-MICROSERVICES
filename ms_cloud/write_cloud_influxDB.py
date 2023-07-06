from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WritePrecision
from datetime import datetime
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
class WriteCloud_InfluxDB:   															# C'É UNA COPIA UGUALE IN DATA PROCESS
	def __init__(self, url, token, org):
		self.influxDB_url = url
		self.influxDB_token = token
		self.influxDB_org = org
		self.client = InfluxDBClient(
			url=self.influxDB_url, token=self.influxDB_token, org=self.influxDB_org, verify_ssl=False, username="ict4bd2", password="YZ5du3XqU$")


	def addMeasurement(self, bucket, name_point, fields = [], tags = [], timestamp = datetime.now() ):
		point = Point(name_point)
		if type(tags) == list:
			for k,v in tags:
				point.tag(k,v) 
		if type(fields) == list:
			for k, v in fields:
				point.field(k,float(v)) 
		elif type(fields) == dict:
			for k, v in fields.items():
				point.field(k,float(v)) 
		else: pass
				
		write_api = self.client.write_api(write_options=SYNCHRONOUS)
		write_api.write(bucket, self.influxDB_org, point)

		file_cloud_log = open('./ms_cloud/cloud.log', 'a')
		# Scrivi la stringa nel file
		mess = f"{{timestamp: {str(datetime.now())}, data: {{"
		if type(fields) == list:
			for k, v in fields:
				mess +=f" {k}: {v}"
		elif type(fields) == dict:
			for k, v in fields.items():
				mess += f" {k}: {v}"
		else: pass
		mess += "}}"
		print(f"{str(datetime.now())} - SENT - {mess}", file=file_cloud_log)

		print("Aggiunta misurazione: ->")
		if type(fields) == list:
			for k, v in fields:
				print(f"\t t: {timestamp}, {k}: {v}")
		elif type(fields) == dict:
			for k, v in fields.items():
				print(f"\t t: {timestamp}, {k}: {v}")
		else: pass
		print()
