from datetime import datetime
import json
import requests
import time
from logging import raiseExceptions

# import json variable names under the variable de
import defines_shared.defineJSONVariables as deJSONVar
de = deJSONVar.de()
class ServiceCatalogueCommunication():
	def __init__(self, setting_path):
		self.settings = json.load(open(setting_path))
		self.name = self.settings[de.name]
		self.localhost = self.settings[de.localhost]
		self.port = self.settings[de.port]

		self.main_ip = self.settings[de.main_ip]
		self.main_port = self.settings[de.main_port]

		self.process_is_on = False
		
		pass
	
	# questo permette di stoppare il thrad lanciatoprecedentemente in un qualsiasi punto del codice esterno al thread
	def stop_thread(self):
		self.process_is_on = False

	def ping_service_catalogue(self):
		# PRIMA SEZIONE PER REGISTRARSI AL CATALOGO
		try:
			self.process_is_on = True
			service = {"id": self.name, "ip": self.localhost, "port": self.port}
			requests.put(f'http://{self.main_ip}:{self.main_port}/ser', json=service)
			while self.process_is_on:
				service = {"id": self.name, "ip": self.localhost, "port": self.port}
				requests.put(f'http://{self.main_ip}:{self.main_port}/ser', json=service)
				print(f"microservizio '{self.name}' postato sul ServiceCatalog")
				print("*",end = "")
				time.sleep(20)
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
		#ip, port = self.GetIpandPort("resource_catalog")
		ip, port = "127.0.0.1", "8082"
		device = {str(devideID): str(datetime.now())}
		requests.put(f'http://{ip}:{port}/{localityID}/ping_res', json=device)
		#requests.put(f'http://127.0.0.2:8082/{localityID}/ping_res', json=device)
		while self.process_is_on:
			device = {str(devideID): str(datetime.now())}
			requests.put(f'http://{ip}:{port}/{localityID}/ping_res', json=device)
			#requests.put(f'http://127.0.0.2:8082/{localityID}/ping_res', json=device)
			print(f"Kit '{devideID}' - Ping to Resource Catalog")
			print(".", end="")
			time.sleep(2)
		'''except:
			print(f"REGISTRATION of'' on Device Catalog FAILED")
			raiseExceptions(f"REGISTRATION of ' on Device Catalog FAILED")
'''
