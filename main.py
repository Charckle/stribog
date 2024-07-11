import os
import time
from modules.pylavor import Pylavor
from modules.email_sender import EmS
from source_script import source_script
import json
import logging
import hashlib
from jinja2 import Environment, FileSystemLoader


date_mod = "28.07.2024"

settings = {}
settings_filename = "conf.json"
settings_last_modified = "banan"

targets = []
targets_filename = "targets.json"
targets_last_modified = "banan"

contacted_admin = False

in_memory_content = []

logger = logging.getLogger(__name__)

def logo():   
    logo_ascii = r"""
---------------------------+
  _________ __         ._____.                  
 /   _____//  |________|__\_ |__   ____   ____  
 \_____  \\   __\_  __ \  || __ \ /  _ \ / ___\ 
 /        \|  |  |  | \/  || \_\ (  <_> ) /_/  >
/_______  /|__|  |__|  |__||___  /\____/\___  / 
        \/                     \/      /_____/  
------------------+
"""
    logger.info(r"---------------------------+")    
    logger.info(r"  _________ __         ._____.                  ")    
    logger.info(r" /   _____//  |________|__\_ |__   ____   ____  ")    
    logger.info(r" \_____  \\   __\_  __ \  || __ \ /  _ \ / ___\ ")    
    logger.info(r" /        \|  |  |  | \/  || \_\ (  <_> ) /_/  >")    
    logger.info(r"/_______  /|__|  |__|  |__||___  /\____/\___  / ")    
    logger.info(r"        \/                     \/      /_____/  ")    
    logger.info(r"------------------+")    

    logger.info("Stribog: A notification system for changes on a specific source")    
    logger.info(f"Version: {get_version()}")    
    logger.info(f"Andrej Zubin - {date_mod}")
    logger.info("--------------------------------------------+ \n")    
    logger.info(f"Instance Name: {settings['instance_name']}")
    logger.info("--------------------------------------------+ \n\n")        


def get_settings_filepath():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), settings_filename)

def get_targets_filepath():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), targets_filename)

def get_version_filepath():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "VERSION")

def get_version():
    version_ = "ERROR"
    file_path = get_version_filepath()
    try:
        with open(file_path, 'r') as file:
            version_ = file.read().strip()
    except FileNotFoundError:
        logger.error(f"Version file not found: {file_path}")            
    except Exception as e:
        logger.error(f"An error occurred: {e}")            
            
    
    return version_

def load_data(file_path):
    # Load data from file
    with open(file_path, 'r') as file:
        data = file.read()
        
    return data


def setup_logging(config):
    logging_level_str = config.get("logging_level", "INFO").upper()
    logging_level = getattr(logging, logging_level_str, logging.INFO)
    logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')
    logger.info(f"Logging Level set to: {logging.getLevelName(logger.getEffectiveLevel())}")    
    


def settings_check():
    global settings_last_modified
    settings_current_modified = os.path.getmtime(get_settings_filepath())
    
    if settings_current_modified != settings_last_modified:
        logger.info(f"File has changed. Reloading config data...")
        settings_load()
        
        
def targets_check():
    global targets_last_modified
    
    targets_current_modified = os.path.getmtime(get_targets_filepath())

    if targets_current_modified != targets_last_modified:
        logger.info(f"File has changed. Reloading targets data...")
        targets_load()
        
        
def load_json_file(filename_):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        json_file = Pylavor.json_read(current_dir, filename_)
    except FileNotFoundError:
        logger.critical(f"Error: File {filename_} not found.")        
        # Stop the program
        exit(1)
    except IOError as e:
        logger.critical(f"Error: Unable to read file {filename_} - {e}")        
        # Stop the program
        exit(1)
    except json.decoder.JSONDecodeError as e:
        # Handle JSON decoding error
        logger.critical(f"Error decoding JSON {filename_}: {e}")
        # Stop the program
        exit(1)  
    
    return json_file

def settings_load():
    global settings_last_modified
    global settings
    
    settings = load_json_file(settings_filename)
    setup_logging(settings)
    settings_last_modified = os.path.getmtime(get_settings_filepath())
    logger.debug(f"Settings loaded successfully")
    
    
    
def targets_load():
    global targets_last_modified
    global targets
    
    targets = load_json_file(targets_filename)
    targets_last_modified = os.path.getmtime(get_targets_filepath())
    logger.debug(f"Targets loaded successfully")


def hash_string(input_string: str) -> str:
    # Create a SHA-256 hash object
    sha256 = hashlib.sha256()
    
    # Encode the input string and update the hash object
    sha256.update(input_string.encode('utf-8'))
    
    # Return the hexadecimal representation of the hash
    return sha256.hexdigest()


def source_check_integrity():
    # check if the source has the required format, meaning it didn't change and the data can be extracted
    logger.debug(f"Checking source integrity.")    
    return source_script.is_source_OK()


def source_get_data():
    global in_memory_content
    in_memory_content_lenght = len(in_memory_content)
    
    # write code to get the data
    source_data = source_script._get_data()#{"topic": "test 1, test2"}
    if source_data == None:
        logger.error(f"No data could be scrapped.")        
        
        return None
    
    modified_data = []
    
    for source_p in source_data:
        hash_s = hash_string(source_p['post_excerpt'])
        memory_string = f"{source_p['post_title']}: {hash_s}"
        
        if memory_string in in_memory_content:
            pass
        else:
            in_memory_content.append(memory_string)
            modified_data.append(source_modify_data_for_message(source_p))

    # if nothing is in memory, dont just send all of them
    if in_memory_content_lenght == 0:
        # if app has nothing in memory, aka restarted, send jut the last one
        if settings["on_no_memory_send_one"]:
            modified_data = [modified_data[-1]]
        else: 
            logger.debug(f"No new content") 
            modified_data = []

    return modified_data

def plain_text_data(source_data):    
    modified_data_p = f"""{settings['message']}: {settings['topic']}
    {source_data['post_title']} . {source_data['post_date']}, - {source_data['post_category']},
    {source_data['post_excerpt']}
    {source_data['post_link']}
    """
    
    return modified_data_p

def html_text_data(source_data):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('templates/base.html')    
    data = {"source_data": source_data,
            "settings": settings}
    
    return template.render(data)

def source_modify_data_for_message(source_data):    
    plain_text_ = plain_text_data(source_data)
    html_text_ = html_text_data(source_data)
    
    return [plain_text_, html_text_]


def notifications_proliferate(source_data):
    global targets
    global settings
    logger.debug(f"Starting notification Proliferation")
    
    
    ems_object = EmS(settings)
            
    if ems_object.check_conn():
        for target in targets:
            receiver_email = target["email"]
            subject =  "Update: " + settings["topic"]

            if target["active"] == True:
                logger.debug(f"sending to: {target['name']}")
                for source_data_p in source_data:
                    simple_text = source_data_p[0]
                    html_text = source_data_p[1]
                    
                    ems_object.send_no_attach(receiver_email, subject, simple_text, html_text)
    
def admin_contact(what_to_say):   
    global settings
    
    receiver_email = settings["admin_email"]
    instance_name = settings["instance_name"]
    
    subject = f"Stribog Error on: {instance_name}"
    simple_text = f"{what_to_say}"
    html_text = simple_text
    
    ems_object = EmS(settings)
    logger.debug(f"Sending to admin")
    logger.debug(what_to_say)
    print("KURAC")
    
    ems_object.send_no_attach(receiver_email, subject, simple_text, html_text)

def first_boot():
    global settings
    global logger

    # load settings
    settings_load()    
    logo()
    
    # load targets
    targets_load()
    # check email server connection
    # emails_check_conn()
    ems_object = EmS(settings)
    logger.debug(f"Checking email server connection")
    is_connected = ems_object.check_conn()
    if is_connected == False:
        logger.critical(f"Error booting up! - shutting down!")
        # Stop the program
        exit(1)
    else:
        logger.debug(f"Connection OK!")
        
        


def main_loop():
    global settings
    global contacted_admin
    
    logger.info(f"Starting main loop")
    
    #time.sleep(3)
    
    while True:
        logger.debug(f"Starting new loop")
        source_data = "No data"
        
        settings_check()
        targets_check()
        
        source_integrity = source_check_integrity()
        
        if not targets_check and contacted_admin == False:
            # contact the admin
            admin_contact("The Source seems to be corrupted.")
            contacted_admin = True
        elif targets_check:
            contacted_admin = False
        
        source_data_modified = source_get_data()

        if source_data_modified:
            notifications_proliferate(source_data_modified)
        
        logger.debug(f"Starting sleep interval")
        time.sleep(settings["source_check_interval"])
        
    

if __name__ == "__main__":
    # first boot setup
    first_boot()
    
    # main loop
    main_loop()