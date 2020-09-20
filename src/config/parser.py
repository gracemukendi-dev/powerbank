'''
    These functions parse values from the $PB_CONFIG_FILE
    which is located at $PB_CONFIG_FILE_LOC. 
'''
import json
import logging

logger = logging.getLogger("root")

def readFile(config_file):
    try:
        with open(config_file, "r") as config_file:
            content = config_file.read()
    except:
        logger.error(f"Error parsing Config file. [{config_file}] was set as config file.")
        return None
        
    return json.loads(content)

def retrieveResources(config_file):
    json_content = readFile(config_file)
    return json_content["resources"]

def retrieveContent(config_file):
    return readFile(config_file)
