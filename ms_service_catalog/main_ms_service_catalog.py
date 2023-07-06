
import os
import sys
#sys.path.append('D:\\POLITECNICO\\Magistrale\\A_IP\\project\\codice\\ms_service_catalog')
# RICORDARE DI TOGLIERRE ms_service_catalog quando si DOCKERIZZA perché cambia la directory principale di lavoro
import defines.define_URIs_service_catalog as deMicroServices
from defines.defineJSONVariables import de as deJSONVar 

import json
import cherrypy
import time


# import json variable names under the variable de
de = deJSONVar()

# import json variable names under the variable de
deMS =  deMicroServices.de_microservices()

# linksmart 
# Azur Iot hub
# cercare task 

# per poter creare l'eseguibile correttamente e funzionante
#application_path = os.path.dirname(sys.executable) #.replace("\\", "/")
application_path = "."

class ServiceCatalog():
	exposed = True
	def __init__(self, path, status):
		self.path = path
		self.status = status

		# reset the service.json information
		f = open(self.path, "w")
		json.dump({
			de.services : []
		}, f)
		f.close()

	@cherrypy.tools.json_out()
	def GET(self, *uri, **param):
		print((uri, list(param.keys())))
		if (uri, list(param.keys())) == deMS.main:
			if self.status:
				return f"microservizio '{__class__.__name__}' -> OK"
			else:
				return f"ERROR PAGE -> {__class__.__name__} loading FAILED"
		elif (uri, list(param.keys())) == deMS.get_service_uri_by_name:
			f = open(self.path, "r")
			services = json.load(f)
			f.close()
			t = time.time()
			for ser in services[de.services]:
				if ser[de.id] == param[de.id]:
					if t - ser[de.timestamp] >= 20:
						services[de.services].remove(ser)
						return {"ser" :de.service_not_present}
						# raise cherrypy.HTTPError(400, "service not found") # la classe non deve lanciare errori 
					else:
						return ser
			return de.service_not_present
			#raise cherrypy.HTTPError(400, "service not found") # la classe non deve lanciare errori
		# ONLY FOR IMPLEMENTATION TIME
		elif (uri, list(param.keys()),) == True:
			print("")
			return True
		# CATCH URI NOT ALLOWED
		else:
			print("ERRORE: URI NON RICONOSCIUTO")
			return de.uri_not_recognized
			#return None
	#@cherrypy.tools.json_in()
	def PUT(self, *uri, **param):
		#print((uri, list(param.keys())))
		if (uri, list(param.keys())) == deMS.put_service_ping:
			f = open(self.path, "r")
			services = json.load(f)
			f.close()
			body = json.loads(cherrypy.request.body.read())
			body[de.timestamp] = time.time()
			for res in services[de.services]:
				if res[de.id] == body[de.id]:
					services[de.services].remove(res) #è possibile che siano cambiati ip e port oltre il timestamp
			services[de.services].append(body)
			f = open(self.path, "w")
			json.dump(services, f)
			f.close()
		# ONLY FOR IMPLEMENTATION TIME
		elif (uri, list(param.keys()),) == True:
			print("")
			return True
		# CATCH URI NOT ALLOWED
		else:
			print("ERRORE: URI NON RICONOSCIUTO")
			return de.uri_not_recognized
			#return None


if __name__ == "__main__":
	settings_path = f"{application_path}/ms_service_catalog/settings.json"
	setting = json.load(open(settings_path))
	
	conf = {
		'/': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on': True,
		}
	}
	status = True

	cherrypy.tree.mount(ServiceCatalog(setting[de.path_services_json],status = status), '/', conf)
	cherrypy.config.update({'server.socket_host': setting[de.localhost]})
	cherrypy.config.update({'server.socket_port': setting[de.port]})

	de.print_name_cmd_2_lines()
	cherrypy.engine.start()
	cherrypy.engine.block()
	t0 = time.time()