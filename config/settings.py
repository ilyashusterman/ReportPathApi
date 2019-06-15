
############################
###  DATAPATH DEFAULTS   ###
############################
import os

MAX_DATABASE_CREATION_ERRORS = 1
NO_ERRORS_OCCURRED = 0




########################################
###    REPORT CONVERTER DEFAULTS     ###
########################################

DEFAULT_SUBTYPE = 'minor'
REPORT_TYPE_ACCIDENT_CRASH = 'crash'
REPORT_TYPE_DEFAULT = 'incident'
DEFAULT_CITY_ORIGIN = 'Las Vegas'
CREATION_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%jZ'
REPORT_DATE_TIME_FORMAT = '%d_%m_%Y %H:%M:%S %Z'

################################
###  REPORT PARSER DEFAULTS  ###
################################

DEFAULT_REPORT_UUID = ''
DEFAULT_REPORT_SYSTEM_ID = ''
DEFAULT_REPORT_RELIABILITY =''
DEFAULT_REPORT_CONFIDENCE = ''
DEFAULT_REPORT_TYPE = ''
DEFAULT_REPORT_DESCRIPTION = ''
DEFAULT_REPORT_DATA_TYPE = ''
DEFAULT_REPORT_SUB_TYPE = ''
REPORT_DEFAULT_X = 1
REPORT_DEFAULT_Y = 1
REPORT_DEFAULT_STREET = ''
DEFAULT_REPORT_LOCATION_DICT = {'x': REPORT_DEFAULT_X, 'y': REPORT_DEFAULT_Y}


##############################################################################
###                             DATABASES                                  ###
##############################################################################

###################
###  FIREBASE   ###
###################
FIREBASE_URL = os.environ.get('FIREBASE_URL', 'https://temp-waycare.firebaseio.com')
DEFAULT_FIREBASE_SECRET = os.environ.get('DEFAULT_FIREBASE_SECRET', '123')
DEFAULT_FIREBASE_EMAIL = os.environ.get('DEFAULT_FIREBASE_EMAIL', 'lala@waycaretech.com')

##################################
###  FIREBASE INPUTS DEFAULTS  ###
##################################
DEFAULT_FIREBASE_REPORT_WEATHER = '0'
DEFAULT_FIREBASE_REPORT_STATE = 'unconfirmed'

###################
###   MONGODB   ###
###################
MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
MONGODB_PORT = int(os.environ.get('MONGODB_PORT', 27017))
MONGODB_NAME = os.environ.get('MONGODB_HOST', 'test_database')



















