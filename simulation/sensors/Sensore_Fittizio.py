import numpy as np
import requests 
from datetime import datetime

import time
from logging import raiseExceptions
class SensoreFittizio():
	def __init__(self, v, minv , maxv, varv = 1, maxIncr = 5):
		self.value = v
		self.minVal = minv
		self.maxVal = maxv
		self.variance = varv
		self.maxIncrement = abs(maxIncr)

		self.process_is_on = False
	def GenerateNewMeasurement(self):
		dt = np.random.normal() * self.variance
		if ( abs(dt) > self.maxIncrement):
			if( dt >= 0):
				dt = + self.maxIncrement
			if( dt < 0):
				dt = - self.maxIncrement
		
		self.value = self.value + dt
		if(self.value > self.maxVal):
			self.value = self.maxVal
		if (self.value < self.minVal):
			self.value = self.minVal
		return self.value
	def ReturnMeasure(self):
		return self.value

	def stop_thread(self):
		self.process_is_on = False
	
	def start_thread(self):
		self.process_is_on = True
	def generate_and_send_data(self, main_ip, main_port, localityID, sensorID):
		# PRIMA SEZIONE PER REGISTRARSI AL CATALOGO
		try:

			self.process_is_on = True
			while self.process_is_on:
				requests.put(f'http://{main_ip}:{main_port}/{localityID}/history/new_influxDB?cks= 1',
				             json={"value": self.GenerateNewMeasurement(), "tag": sensorID})
				print("-", end="")
				time.sleep(4)
		except:
			print(f"REGISTRATION of'' on Service Catalog FAILED")
			raiseExceptions(f"REGISTRATION of'' on Service Catalog FAILED")
