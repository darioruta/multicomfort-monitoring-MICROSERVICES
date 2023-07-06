


class de ():

    '''

    Class dedicated to 'store' globals definitions of variables

    '''

    def __init__(self):
    



        self.sensors_catalog_ID = "sensors_catalogID"
        self.sensors = "sensors"
        self.sensorID = "sensorID"
        self.data = "data"
        self.temperature = "temperature"
        self.humidity = "humidity"
        self.deepsensor = "deepsensor"
        self.slopes = "slopes"
        
        self.info_client= "info_client"
        self.sensor_name = "sensor_name"
        self.sensor_model = "sensor_model"
        self.date_assembly = "date_assembly"
        


        self.localityName = "localityName"
        self.path = "path"
        self.num_slopes = "num_slopes"
        
        self.localities = "localities"
        self.localityID = "localityID"
        self.info = "info"
        self.mslm = "mslm"
        
        self.slopes = "slopes"
        self.slopeID = "slopeID"
        self.sectors = "sectors"
        self.sectorID = "sectorID"
        
        self.timestamp = "timestamp"


        
        
        self.cannons = "cannons"

        self.cannons_catalog_ID = "cannons_catalog_ID"
        self.cannonID = "cannonID"
        self.type = "type"
        self.mode = "mode"
        self.state = "state"
        self.info = "info"
        self.prog_on = "prog-on"
        self.prog_off = "prog-off"
        self.auto_threshold = "auto-threshold"
        self.info_client = "info_client"
        self.cannon_name = "cannon_name"
        self.cannon_model = "cannon_model"
        self.water_volume = "water_volume(l)"


        self.NoInformation = "NoInformation"

        self.path_services_json = "path_services_json"

        #self. = ""
        
        self.name = "name"
        self.localhost = "localhost"
        self.port = "port"
        self.ip = "ip"
        self.main_ip = "main_ip"
        self.main_port = "main_port"

        self.token_telegram_bot = "token_telegram_bot"
        
        self.world_path = "./data/stored/world.json"

        self.world_localities_path = "./ms_resource_catalog/data/world_locality.json"
        self.settings_path = "./settings.json"
        
        #self.cat_loc_1_PATH = "./data/stored/locality_catalog.json"
        #self.cat_cannons_1_PATH = "./data/stored/cannons_catalog.json"
        #self.cat_sensors_1_PATH = "./data/stored/sensors_catalog.json"
        
        self.cat_loc_1_PATH = "./data/stored_test/locality_catalog.json"
        self.cat_cannons_1_PATH = "./data/stored_test/cannons_catalog.json"
        self.cat_sensors_1_PATH = "./data/stored_test/sensors_catalog.json"
        
        self.data_recorded_path =  "./data/stored/data_recorded.json"
        
        self.path_end_cannons = "/cannons_catalog.json"
        self.path_end_sensors = "/sensors_catalog.json"
        self.path_end_locality = "/locality_catalog.json"
        self.path_end_history = "/history.json"

        #constant
        self.ID_default = 1
        
        self.FORMAT_INT = 0
        self.FORMAT_FLOAT = 1
        self.FORMAT_STRING = 2
        
        self.cannonTypesPossible = ["mobile,fisso"]
        self.cannonModePossible = ["auto","manual","off"]
        self.cannonStatePossible = ["off", "on"]
        
