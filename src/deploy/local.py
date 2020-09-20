'''
    This class keeps the state of local deployments.
    Local Deployment states consist of:
        * Corresponding pwb config files
        * Corresponding terraform files
    Note: This class structure and utility is still under construction
    may be changed in the future.
'''
import os 
import random
import logging

logger = logging.getLogger('root')

class PWB_Local():
    def __init__(self, config_file_loc, file_content):
        self.id = random.randint(0,10)
        self.config_file_loc = config_file_loc
        self.configuration = None
        self.configuration = Configuration(file_content)
    
    def run(self):
        logger.info("+++Installing localstack+++")
        os.system("/vagrant/src/scripts/localstack.sh")
        logger.info("+++Running terraform for local resources+++")
        for resource in self.configuration.resources:
            os.system(f"/vagrant/src/scripts/terraform.sh {resource}")
        
class Configuration():
    def __init__(self, file_content):
        self.resources = file_content["resources"]

