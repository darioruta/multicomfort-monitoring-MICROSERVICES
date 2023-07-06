import paho.mqtt.client as mqtt
import json
# file dedicato all'interfaccia MQTT
# file dedicato all'interfaccia REST


import defines.defineJSONVariables as deJSONVar
from datetime import datetime


import defines.defineExceptions as deExcept
import defineURIMicroservices as deMicroServices
from bibliotecario import bibliotecario
deMS = deMicroServices.de_microservices()

ex = deExcept.Exception()
de = deJSONVar.de()
class MQTTCloud:  

	def __init__(self, biblio, localityName, localityID, broker_address, broker_port):
		self.bi: bibliotecario = biblio
		self.localityName = localityName
		self.localityID = localityID


		self.client = mqtt.Client()
		self.client.on_message = self.on_message
		self.client.connect(broker_address, broker_port)
		self.state_mqtt = False
		pass

	def on_message_original(self,client, userdata, message):
		print("Message Received!")
		print("  topic :", message.topic)
		message_arrived = str(message.payload.decode("utf-8"))
		print("  messaggio:", message_arrived)
		with open('messages.txt', 'a') as file:
			# Scrivi la stringa nel file
			print(message_arrived, file=file)

	def on_message(self,client, userdata, message):
		#print("Message Received!")
		#print("  topic :", message.topic)
		try:
			message_arrived = str(message.payload.decode("utf-8"))
			file_cloud_log = open('./ms_cloud/cloud.log', 'a')
			# Scrivi la stringa nel file
			print(f"{str(datetime.now())} - RECEIVED - {message_arrived}", file=file_cloud_log)
			if message_arrived == "": 
				print(f"\nERRORE - File vuoto (message_arrived = "")", file=file_cloud_log)
				return # se il messaggio é vuoto esco dalla funzione
			if message_arrived == None: 
				print(f"\nERRORE - File vuoto (message_arrived = None)", file=file_cloud_log)
				return # se il messaggio é None esco dalla funzione

			file_cloud_log.close()

			print("  messaggio:", message_arrived)
			message_arrived = message_arrived.replace("nan", '-3.141592')

			print("  messaggio updated:", message_arrived)
			json_data = json.loads(message_arrived)
			print(f"Loc -> {self.localityName} -> json_data in ingresso: {json_data}", end = "\n\n")
			measurements = json_data["data"]
			tags = [("kitID", json_data["kitID"])]
			self.bi.addMeasurements_InfluxDB(measurements, tags, bucket=de.bucket_Io3_raw_data) # , timestamp=json_data["timestamp"]
		except:
			pass
		
		#for k,v in json_data.items():
	#		print(f"key: {k}\tvalue: {v}")

	def subscribe(self, topic):
		print( f"Mi sottoscrivo al topic: ->{topic}<-")
		self.client.subscribe(topic)

	def start(self):
		print("Mi metto in ascolto")
		self.state_mqtt = True
		while self.state_mqtt:
			self.client.loop()

		self.client.disconnect()
	def stop_subscription(self):
		self.state_mqtt = False

	# qua vanno inseriti tutti i metodi riguardanti la comunicazione attraverso MQTT
	#  


