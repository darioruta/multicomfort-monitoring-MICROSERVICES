from datetime import datetime
import json
import requests
import time
from logging import raiseExceptions

# import json variable names under the variable de
import defines_shared.defineJSONVariables as deJSONVar
de = deJSONVar.de()
class AutoGenerationSimulationProcess():
	def __init__(self):
		self.process_is_on = False
		
		pass
	
	# questo permette di stoppare il thrad lanciatoprecedentemente in un qualsiasi punto del codice esterno al thread
	def stop_thread(self):
		self.process_is_on = False

	def generate_and_send_data(self):
		# PRIMA SEZIONE PER REGISTRARSI AL CATALOGO
		try:
			self.process_is_on = True
			service = {"id": self.name, "ip": self.localhost, "port": self.port}
			requests.put(f'http://{self.main_ip}:{self.main_port}/ser', json=service)
			while self.process_is_on:
				service = {"id": self.name, "ip": self.localhost, "port": self.port}
				requests.put(f'http://{self.main_ip}:{self.main_port}/ser', json=service)
				#print(f"microservizio '{self.name}' postato sul ServiceCatalog")
				print("*",end = "")
				time.sleep(10)
		except:
			print(f"REGISTRATION of'' on Service Catalog FAILED")
			raiseExceptions(f"REGISTRATION of'' on Service Catalog FAILED")

	def GetIpandPort(self, name):
		try:
			info = requests.get(f'http://{self.main_ip}:{self.main_port}/get', params=[("id", name),]).json()
			return info[de.ip], info[de.port]
		except:
			print(f"Get information from Service Catalog by '{self.name}' FAILED")
			raiseExceptions(f"Get information from Service Catalog by FAILED")

	def ping_device_catalogue(self, localityID, devideID):
		# PRIMA SEZIONE PER REGISTRARSI AL CATALOGO
		self.process_is_on = True
		ip, port = self.GetIpandPort("resource_catalog")
		device = {str(devideID): str(datetime.now())}
		requests.put(f'http://{ip}:{port}/{localityID}/ping_res', json=device)
		#requests.put(f'http://127.0.0.2:8082/{localityID}/ping_res', json=device)
		while self.process_is_on:
			device = {str(devideID): str(datetime.now())}
			requests.put(f'http://{ip}:{port}/{localityID}/ping_res', json=device)
			#requests.put(f'http://127.0.0.2:8082/{localityID}/ping_res', json=device)
			#print(f"microservizio '{self.name}' postato sul ServiceCatalog")
			print(".", end="")
			time.sleep(2)
		'''except:
			print(f"REGISTRATION of'' on Device Catalog FAILED")
			raiseExceptions(f"REGISTRATION of ' on Device Catalog FAILED")
'''
