


class de ():

    '''

    Class dedicated to 'store' globals definitions of variables

    '''

    def __init__(self):
        
        self.name = "name"
        self.localhost = "localhost"
        self.port = "port"
        self.ip = "ip"
        self.main_ip = "main_ip"
        self.main_port = "main_port"


        self.kits_catalog_ID = "kits_catalogID"
        self.kits = "kits"
        self.kitID = "kitID"
        self.kit_MAC = "kit_MAC"
        self.data = "data"
        self.temperature = "temperature"
        self.humidity = "humidity"
        self.deepsensor = "deepsensor"
        self.plessi = "plessi"
        
        self.info_client= "info_client"
        self.kit_name = "kit_name"
        self.kit_model = "kit_model"
        self.date_assembly = "date_assembly"
        


        self.localityName = "localityName"
        self.path = "path"
        self.num_plessi = "num_plessi"
        
        self.localities = "localities"
        self.localityID = "localityID"
        self.info = "info"
        self.mslm = "mslm"
        
        self.plessoID = "plessoID"
        self.plessoName = "plessoName"
        self.aule = "aule"
        self.aulaID = "aulaID"
        self.aulaName = "aulaName"
        
        self.timestamp = "timestamp"


        
        # per attuatori
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

        self.cannonTypesPossible = ["mobile,fisso"]
        self.cannonModePossible = ["auto", "manual", "off"]
        self.cannonStatePossible = ["off", "on"]
        # fine attuatori


        self.NoInformation = "NoInformation"

        self.path_services_json = "path_services_json"

        #self. = ""
        

        self.token_telegram_bot = "token_telegram_bot"
        
        self.world_path = "./data/stored/world.json"

        self.world_localities_path = "./ms_resource_catalog/data/world_locality.json"
        self.settings_path = "./settings.json"
        
        self.cat_loc_1_PATH = "./data/stored_test/locality_catalog.json"
        self.cat_cannons_1_PATH = "./data/stored_test/cannons_catalog.json"
        self.cat_sensors_1_PATH = "./data/stored_test/sensors_catalog.json"
        
        self.data_recorded_path =  "./data/stored/data_recorded.json"
        
        self.path_end_cannons = "/cannons_catalog.json"
        self.path_end_sensors = "/sensors_catalog.json"
        self.path_end_locality = "/locality_catalog.json"
        self.path_end_history = "/history.json"
        self.path_end_dev_cat = "/dev_cat.json"

        self.broker_address = "broker_address"
        self.broker_port = "broker_port"
        self.topic_subscribe = "topic_subscribe"

        # CONSTANTS
        self.ID_default = 1
        
        self.FORMAT_INT = 0
        self.FORMAT_FLOAT = 1
        self.FORMAT_STRING = 2
        
    def print_name_cmd_2_lines(self):
        print("\n\
             _______  _______  _______  _______           _______  _______  _______  \n\
            (  ____ )(  ____ \(  ____ \(  ___  )|\     /|(  ____ )(  ____ \(  ____ \ \n\
            | (    )|| (    \/| (    \/| (   ) || )   ( || (    )|| (    \/| (    \/ \n\
            | (____)|| (__    | (_____ | |   | || |   | || (____)|| |      | (__     \n\
            |     __)|  __)   (_____  )| |   | || |   | ||     __)| |      |  __)    \n\
            | (\ (   | (            ) || |   | || |   | || (\ (   | |      | (       \n\
            | ) \ \__| (____/\/\____) || (___) || (___) || ) \ \__| (____/\| (____/\ \n\
            |/   \__/(_______/\_______)(_______)(_______)|/   \__/(_______/(_______/")
        print("\n \
                 _______  _______ _________ _______  _        _______  _______  \n\
                (  ____ \(  ___  )\__   __/(  ___  )( \      (  ___  )(  ____ \ \n\
                | (    \/| (   ) |   ) (   | (   ) || (      | (   ) || (    \/ \n\
                | |      | (___) |   | |   | (___) || |      | |   | || |       \n\
                | |      |  ___  |   | |   |  ___  || |      | |   | || | ____  \n\
                | |      | (   ) |   | |   | (   ) || |      | |   | || | \_  )   \n\
                | (____/\| )   ( |   | |   | )   ( || (____/\| (___) || (___) | \n\
                (_______/|/     \|   )_(   |/     \|(_______/(_______)(_______)\n")
        
