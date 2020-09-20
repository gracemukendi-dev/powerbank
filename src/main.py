import log
logger = log.setup_custom_logger('root')

from deploy import local
from config import parser
import os

def deploy():
    config_file_loc = os.getenv("PWB_CONFIG_FILE_LOC", "/vagrant/config.json")
    logger.debug(f"File loc is {config_file_loc}")
    file_content = parser.retrieveContent(config_file_loc)

    if(file_content != None):
        local_deployment = local.PWB_Local(config_file_loc, file_content)
    else:
        logger.error("No file content loaded.")
    
    if(local_deployment != None):
        logger.info(f"Local Deployment Success! The config content is set to {local_deployment.configuration.resources}")
    else:
        logger.error(f"Local Deployment Failed!")
    return local_deployment

if(__name__ == "__main__"):
    local_dep = deploy()
    local_dep.run()
