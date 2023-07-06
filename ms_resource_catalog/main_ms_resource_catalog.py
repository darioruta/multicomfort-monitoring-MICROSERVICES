# 1600 lines 
import threading
from logging import raiseExceptions
import time
import requests
import cherrypy
import os,os.path
import json
import REST_resource_catalog as Rrc
import MQTT_resource_catalogue as MQTTrc
from burattinaio import burattinaio
import lib.json_utilization as ju

# import json variable names under the variable de
import defines.defineJSONVariables as deJSON
de = deJSON.de()

import sys
#sys.path.append('D:\\POLITECNICO\\Magistrale\\A_IP\\project\\codice')
sys.path.append(os.path.abspath(os.getcwd()))
from communication_service_catalogue import ServiceCatalogueCommunication
from manage_world import ManageWorld


import numpy as np

if __name__=="__main__":
	settings_path = "./ms_resource_catalog/settings.json"
	setting = json.load(open(settings_path))
	world_locality_info = json.load(open(de.world_localities_path))





	# appendo il log automatico dopo ogni X secondi al service Catalog
	# process Retrieve Data
	scc = ServiceCatalogueCommunication(settings_path)
	updateServiceCatalog = threading.Thread(target=scc.ping_service_catalogue, name=setting[de.name])  # ricordarsi che non ci vanno i parametri , é come se fosse un altro main doe devi andarti a prendere le info direttamente da la 
	# PING DISATTIVATO
	'''updateServiceCatalog.start()'''
	#updateServiceCatalog.start()

	#print("facciamo qualcosa")
	#time.sleep(30)
	# IMPO    scc.stop_thread()   # questo permette di stoppare il thrad lanciatoprecedentemente in un qualsiasi punto del codice esterno al thread
	#time.sleep(60)

	
	
	
	

	# parte dedicata a REST
	static_dir = os.path.dirname(os.path.abspath(__file__))  # Root static dir is this file's directory.
	conf={
		'/':{
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on':True,
			#'tools.staticdir.root':os.path.abspath(os.getcwd())   # ORIGIANL
			'tools.staticdir.root': static_dir
		},
		'/static':{
			'tools.staticdir.on':True,
			'tools.staticdir.dir':static_dir + '\\templates\\static',
			'tools.staticdir.debug' : True,
			'log.screen' : True
		}
	}
	tutto_ok = False
	mw = ManageWorld(de.world_localities_path)

	if len(np.unique([s[de.path] for s in world_locality_info[de.localities]])) != len(world_locality_info[de.localities]):
		print("error loading the sensorIDs -> there is a repetition of the same sensorID")
	else:
		for ind,s in enumerate(world_locality_info[de.localities]):
			
			path,ID = mw.GetPathByLocalityID(s[de.localityID])	
			bu = burattinaio(path)
			# REST API 
			cherrypy.tree.mount(Rrc.REST_resource_catalog(bu), f'/{ID}', conf)

			# MQTT API
			# parte dedicata a MQTT (se necessaria per i sensori)
			mqtt_API = MQTTrc.MQTT_resource_catalogue(bu, setting[de.broker_address], setting[de.broker_port])
			mqtt_API.subscribe(setting[de.topic_subscribe])
			
			mqtt_subscription = threading.Thread(target=mqtt_API.start)  
			# PING DISATTIVATO
			mqtt_subscription.start()

		tutto_ok = True
	
	cherrypy.tree.mount(Rrc.REST_resource_catalog_default(tutto_ok), '/', conf)

	# OLD
	#cherrypy.tree.mount(RSS.RESTSlopeService(bu),'/',conf)
	cherrypy.config.update(
		{'server.socket_host': setting[de.localhost], 'server.socket_port': setting[de.port]})
	#cherrypy.tree.mount(RSS.RESTSlopeService(),'/Slope_Service',conf)

	#de.print_name_cmd()
	de.print_name_cmd_2_lines()
	cherrypy.engine.start()
	cherrypy.engine.block()

