import logging as log

"""
Settings file for the ltpy module
"""

LOG_LEVEL = log.INFO
LOG_TYPE = 'terminal'       # ['terminal', 'file']
LOG_FILE = 'ltpy.log'       # log file path
LT_HOST = 'xxx.xxx.xxx.xxx' # IP used to connect to the LT ['string']
LT_PORT = '8080'            # Port used to connect to the LT ['string']
PKLFILE = 'submitted'       # Name of pickle file for storing observation information ['string']
DEFAULT_DATADIR = './'      # Path to the directory for storing data.
SAVE_RTML = False           # Whether to save the Request and response [True, False]
