


class de ():

    '''

    Class dedicated to 'store' globals definitions of variables

    '''

    def __init__(self):
        #self. = ""
        
        self.name = "name"
        self.localhost = "localhost"
        self.port = "port"
        self.ip = "ip"
        self.main_ip = "main_ip"
        self.main_port = "main_port"

        self.path_services_json = "path_services_json"

        self.services = "services"
        self.id = "id"
        self.timestamp = "timestamp"

        self.service_not_present = "service_not_present"
        self.uri_not_recognized = "uri_not_recognized"

        self.bucket_Io3_raw_data = "Io3_raw_data"
        self.bucket_Io3_processed_data = "Io3_processed_data"
        self.bucket_Io3_Test1 = "Io3_Test1"

        self.kitID = "kitID"

    def print_name_cmd_2_lines(self):
        print(" \n\
     ______   _______ _________ _______      _______  _______  _______  _______  _______  _______  _______  \n\
    (  __  \ (  ___  )\__   __/(  ___  )    (  ____ )(  ____ )(  ___  )(  ____ \(  ____ \(  ____ \(  ____ \ \n\
    | (  \  )| (   ) |   ) (   | (   ) |    | (    )|| (    )|| (   ) || (    \/| (    \/| (    \/| (    \/ \n\
    | |   ) || (___) |   | |   | (___) |    | (____)|| (____)|| |   | || |      | (__    | (_____ | (_____  \n\
    | |   | ||  ___  |   | |   |  ___  |    |  _____)|     __)| |   | || |      |  __)   (_____  )(_____  ) \n\
    | |   ) || (   ) |   | |   | (   ) |    | (      | (\ (   | |   | || |      | (            ) |      ) | \n\
    | (__/  )| )   ( |   | |   | )   ( |    | )      | ) \ \__| (___) || (____/\| (____/\/\____) |/\____) | \n\
    (______/ |/     \|   )_(   |/     \|    |/       |/   \__/(_______)(_______/(_______/\_______)\_______)\n")