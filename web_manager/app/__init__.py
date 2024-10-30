# Import flask and template operators
from flask import Flask, render_template, jsonify, send_from_directory
from os import path, mkdir, environ 
import logging
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

from app.main_page_module.other import Randoms
from app.pylavor import Pylavor

#from app.main_page_module.argus import WSearch

# Define the WSGI application object
app = Flask(__name__)

targets_ram = []


# load the .env environment variables
load_dotenv()

# Configurations
if environ.get('ENVCONFIG', "DEV") != 'PROD':
    app.config.from_object("config.DevelopmentConfig")
else:
    app.config.from_object("config.ProductionConfig")

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404



# Import a module / component using its blueprint handler variable (mod_auth)
from app.main_page_module.controllers.controllers import main_page_module as main_module


# Register blueprint(s)
app.register_blueprint(main_module)
# app.register_blueprint(xyz_module)
# ..

# activate logging
#app.logger.setLevel(logging.INFO)

logging_level_str = app.config['APP_LOGGING']
logging_level = getattr(logging, logging_level_str, logging.INFO)
app.logger.setLevel(logging_level)

#logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')
#app.logger.info(f"Logging Level set to: {logging.getLevelName(app.logger.getEffectiveLevel())}")

app.logger.info('Application startup')

logo_ascii = r"""
---------------------------+
  _________ __         ._____.                      _____                                             
 /   _____//  |________|__\_ |__   ____   ____     /     \ _____    ____ _____     ____   ___________ 
 \_____  \\   __\_  __ \  || __ \ /  _ \ / ___\   /  \ /  \\__  \  /    \\__  \   / ___\_/ __ \_  __ \
 /        \|  |  |  | \/  || \_\ (  <_> ) /_/  > /    Y    \/ __ \|   |  \/ __ \_/ /_/  >  ___/|  | \/
/_______  /|__|  |__|  |__||___  /\____/\___  /  \____|__  (____  /___|  (____  /\___  / \___  >__|   
        \/                     \/      /_____/           \/     \/     \/     \//_____/      \/       
------------------+
"""
app.logger.info(r"---------------------------+")    
app.logger.info(r"  _________ __         ._____.                      _____                                             ")    
app.logger.info(r" /   _____//  |________|__\_ |__   ____   ____     /     \ _____    ____ _____     ____   ___________ ")    
app.logger.info(r" \_____  \\   __\_  __ \  || __ \ /  _ \ / ___\   /  \ /  \\__  \  /    \\__  \   / ___\_/ __ \_  __ \ ")    
app.logger.info(r" /        \|  |  |  | \/  || \_\ (  <_> ) /_/  > /    Y    \/ __ \|   |  \/ __ \_/ /_/  >  ___/|  | \/")    
app.logger.info(r"/_______  /|__|  |__|  |__||___  /\____/\___  /  \____|__  (____  /___|  (____  /\___  / \___  >__|   ")    
app.logger.info(r"        \/                     \/      /_____/           \/     \/     \/     \//_____/      \/       ")    
app.logger.info(r"------------------+")    

app.logger.info("Stribog Manager: Web Manager for Stribog")    
app.logger.info(f"Version: {Randoms.get_version()}")    
app.logger.info("--------------------------------------------+ \n")    
app.logger.info(f"Instance Name: {app.config['APP_NAME']}")
app.logger.info(f"Logging Level: {logging.getLevelName(app.logger.getEffectiveLevel())}")
app.logger.info("--------------------------------------------+ \n\n")