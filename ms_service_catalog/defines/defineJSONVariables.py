


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

    # link della pagina...
    def print_name_cmd_2_lines(self):
        print(" \n\
                 _______  _______  _______          _________ _______  _______   \n\
                (  ____ \(  ____ \(  ____ )|\     /|\__   __/(  ____ \(  ____ \  \n\
                | (    \/| (    \/| (    )|| )   ( |   ) (   | (    \/| (    \/  \n\
                | (_____ | (__    | (____)|| |   | |   | |   | |      | (__      \n\
                (_____  )|  __)   |     __)( (   ) )   | |   | |      |  __)     \n\
                      ) || (      | (\ (    \ \_/ /    | |   | |      | (        \n\
                /\____) || (____/\| ) \ \__  \   /  ___) (___| (____/\| (____/\  \n\
                \_______)(_______/|/   \__/   \_/   \_______/(_______/(_______/  \n")
        print("\n \
                 _______  _______ _________ _______  _        _______  _______  \n\
                (  ____ \(  ___  )\__   __/(  ___  )( \      (  ___  )(  ____ \ \n\
                | (    \/| (   ) |   ) (   | (   ) || (      | (   ) || (    \/ \n\
                | |      | (___) |   | |   | (___) || |      | |   | || |       \n\
                | |      |  ___  |   | |   |  ___  || |      | |   | || | ____  \n\
                | |      | (   ) |   | |   | (   ) || |      | |   | || | \_  )   \n\
                | (____/\| )   ( |   | |   | )   ( || (____/\| (___) || (___) | \n\
                (_______/|/     \|   )_(   |/     \|(_______/(_______)(_______)\n")
