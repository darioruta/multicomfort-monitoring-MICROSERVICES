# TOT 800 lines



import numpy as np
from defines.defineJSONVariables  import de as deJSONVar
import cherrypy
import os
import os.path
import json
import threading

from bibliotecario import bibliotecario
from REST_cloud import RESTCloud, RESTCloudDefault
import MQTT_cloud as MQTTc
from communication_service_catalogue import ServiceCatalogueCommunication
#de = defineVariable.de()
import defines.defineJSONVariables as deJSONVar
de = deJSONVar.de()

import sys
#sys.path.append('D:\\POLITECNICO\\Magistrale\\A_IP\\project\\codice')
from communication_service_catalogue import ServiceCatalogueCommunication
from manage_world import ManageWorld

if __name__ == "__main__":
	path = "./ms_cloud/settings.json"
	setting = json.load(open(path))
	world_locality_info = json.load(open(de.world_localities_path))
	influxDB_settings = {de.influxDB_token: setting[de.influxDB_token],
                    de.influxDB_url: setting[de.influxDB_url],
                    de.influxDB_org: setting[de.influxDB_org]}

	# multi thread per avere il ping sul Service Catalog
	scc = ServiceCatalogueCommunication(path)
	updateServiceCatalog = threading.Thread(
		target=scc.ping_service_catalogue, name="PingToServiceCatalog")
	# PING DISATTIVATO
	'''updateServiceCatalog.start()'''



	# parte dedicata a MQTT (se necessaria per i sensori)

	# parte dedicata a REST
	# Root static dir is this file's directory.
	static_dir = os.path.dirname(os.path.abspath(__file__))
	'''conf = {
		'/': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on': True,
			#'tools.staticdir.root':os.path.abspath(os.getcwd())   # ORIGIANL
			'tools.staticdir.root': static_dir
		},
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': static_dir + '\\templates\\static',
			'tools.staticdir.debug': True,
			'log.screen': True
		}
	}'''
	conf = {
		'/': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on': True,
		}
	}
	tutto_ok = False
	mw = ManageWorld(de.world_localities_path)

	if len(np.unique([s[de.path] for s in world_locality_info[de.localities]])) != len(world_locality_info[de.localities]):
		print("error loading the sensorIDs -> there is a repetition of the same sensorID")
	else:
		for ind, s in enumerate(world_locality_info[de.localities]):

			path, ID = mw.GetPathByLocalityID(s[de.localityID])
			localityName = mw.NameLocalityByLocalityID(ID)
			#bi = bibliotecario(path, influxDB_settings)
			bi = bibliotecario(path, influxDB_settings)
			print(f"Mounted Locality: {localityName} at localhost:port/{ID}/")

			# REST API
			cherrypy.tree.mount(RESTCloud(bi, localityName, ID), f'/{ID}', conf)

			# MQTT API
			# parte dedicata a MQTT (se necessaria per i sensori)
			mqtt_API = MQTTc.MQTTCloud(bi,localityName, ID, setting[de.broker_address], setting[de.broker_port])
			final_subtopic = "_".join(localityName.split(" "))
			mqtt_API.subscribe(setting[de.topic_subscribe]+f"_{final_subtopic}")
			
			mqtt_subscription = threading.Thread(target=mqtt_API.start)  
			# PING DISATTIVATO
			mqtt_subscription.start()
		tutto_ok = True

	cherrypy.tree.mount(RESTCloudDefault(tutto_ok), '/', conf)

	cherrypy.config.update(
		{'server.socket_host': setting[de.localhost], 'server.socket_port': setting[de.port]})
	#cherrypy.tree.mount(RSS.RESTSlopeService(),'/Slope_Service',conf)
	de.print_name_cmd_2_lines()
	cherrypy.engine.start()
	cherrypy.engine.block()
