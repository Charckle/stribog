import os
import time
from modules.pylavor import Pylavor
from modules.email_sender import EmS
import json

version_ = "0.0.1"

settings = {}
settings_filename = "conf.json"
settings_last_modified = "banan"

targets = []
targets_filename = "targets.json"
targets_last_modified = "banan"

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
    print(logo_ascii)
    print("Stribog: A notification system for changes on a specific source")
    print(f"Version: {version_}")    
    print(f"Andrej Zubin - 6.5.2024")
    print("--------------------------------------------+ \n\n")

def log_update(string_):
    print("--------- -- --------")
    print(string_)
    print("--------- -- --------")


def get_settings_filepath():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), settings_filename)

def get_settings_filepath():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), targets_filename)

def load_data(file_path):
    # Load data from file
    with open(file_path, 'r') as file:
        data = file.read()
        
    return data


def settings_check():
    global settings_last_modified
    settings_current_modified = os.path.getmtime(get_settings_filepath())
    
    if settings_current_modified != settings_last_modified:
        print("File has changed. Reloading config data...")
        
        settings_load()
        
        
def targets_check():
    global targets_last_modified
    
    targets_current_modified = os.path.getmtime(get_settings_filepath())

    if targets_current_modified != targets_last_modified:
        print("File has changed. Reloading targets data...")
        
        targets_load()
        
        
def load_json_file(filename_):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        json_file = Pylavor.json_read(current_dir, filename_)
    except FileNotFoundError:
        log_update(f"Error: File {filename_} not found.")
        # Stop the program
        exit(1)
    except IOError as e:
        log_update(f"Error: Unable to read file {filename_} - {e}")
        # Stop the program
        exit(1)
    except json.decoder.JSONDecodeError as e:
        # Handle JSON decoding error
        log_update(f"Error decoding JSON {filename_}: {e}")    
        # Stop the program
        exit(1)  
        
    return json_file

def settings_load():
    global settings_last_modified
    global settings
    
    settings = load_json_file(settings_filename)
    
    settings_last_modified = os.path.getmtime(get_settings_filepath())
    log_update("Settings loaded successfully")
    
    
def targets_load():
    global targets_last_modified
    global targets
    
    targets = load_json_file(targets_filename)
    
    targets_last_modified = os.path.getmtime(get_settings_filepath())

    log_update("Targets loaded successfully")    


def source_check_integrity():
    # check if the source has the required format, meaning it didn't change and the data can be extracted
    return True


def source_get_data():
    # write code to get the data
    source_data = {"topic": "test 1, test2"}
    
    modified_data = source_modify_data_for_message(source_data)
    
    return modified_data

def source_modify_data_for_message(source_data):
    global settings
    
    modified_data = f"{settings["message"]}: {settings["topic"]}: {source_data["topic"]}"
    return modified_data


def notifications_proliferate(source_data):
    global targets
    global settings
    
    ems_object = EmS(settings)
            
    if ems_object.check_conn():
        for target in targets:
            receiver_email = target["email"]
            subject =  "Update: " + settings["topic"]
            simple_text = source_data
            html_text = simple_text
            
            if target["active"] == True:
                print(simple_text)
                #ems_object.send_no_attach(receiver_email, subject, simple_text, html_text)
    
def admin_contact(what_to_say):
    global settings
    
    receiver_email = target["admin_email"]
    subject = f"Stribog Error on: {instance_name}"
    simple_text = f"{what_to_say}"
    html_text = simple_text
    
    ems_object = EmS(settings)
    print(simple_text)
    #ems_object.send_no_attach(receiver_email, subject, simple_text, html_text)

def first_boot():
    global settings
    
    logo()
    # load settings
    settings_load()

    print(f"Instance Name: {settings['instance_name']}")
    print("--------------------------------------------------------+ \n\n")    
    # load targets
    targets_load()
    # check email server connection
    # emails_check_conn()
    ems_object = EmS(settings)
    ems_object.check_conn()


def main_loop():
    global settings
    
    log_update("Starting main loop")
    time.sleep(3)
    
    while True:
        source_data = "No data"
        
        settings_check()
        targets_check()
        
        source_OK = source_check_integrity()
        if not source_OK:
            # contact the admin
            admin_contact("The Source seems to be corrupted.")
        
        source_data = source_get_data()
        if source_data:
            notifications_proliferate(source_data)
            
        time.sleep(settings["source_check_interval"])
        
    

if __name__ == "__main__":
    # first boot setup
    first_boot()
    
    # main loop
    main_loop()