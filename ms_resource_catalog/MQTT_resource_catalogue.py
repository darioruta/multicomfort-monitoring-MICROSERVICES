import paho.mqtt.client as mqtt
import defines.defineExceptions as deExcept
import json
import burattinaio

# import json variable names under the variable de
import defines.defineURIMicroservices as deMicroServices
deMS = deMicroServices.de_microservices()


# import json variable names under the variable de
# NON UTILIZZATO PER ORA 
import defines.defineJSONVariables as deJSONVar
de = deJSONVar.de()

ex = deExcept.Exception()

class MQTT_resource_catalogue:
	def __init__(self, burattinaio, broker_address, broker_port):
		self.bu = burattinaio
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
		message_arrived = str(message.payload.decode("utf-8"))
		#print("  messaggio:", message_arrived)

		json_data = json.loads(message_arrived)
		
		print(f"json_data in ingresso: {json_data}")
		#for k,v in json_data.items():
		#	print(f"key: {k}\tvalue: {v}")
		#print(f"JSON data: {json_data['1']}")

	def subscribe(self, topic):
		print( f"Mi sottoscrivo al topic: {topic}")
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