'''
    Global configuration.
'''
import logging

logger = logging.getLogger('root')

__pwb_base_dir__    = "/vagrant"
__pwb_src_dir__     = f"{__pwb_base_dir__}/src"
__pwb_config_dir__  = f"{__pwb_src_dir__}/config"
__pwb_scripts_dir__ = f"{__pwb_src_dir__}/scripts"

logger.info(f"__pwb_base_dir : {__pwb_base_dir__}")
logger.info(f"__pwb_src_dir : {__pwb_src_dir__}")
logger.info(f"__pwb_config_dir : {__pwb_config_dir__}")
logger.info(f"__pwb_scripts_dir : {__pwb_scripts_dir__}")
