env = "DEVELOPMENT"
PRODUCTION_SERVER= "172.17.4.154" # Un exemple
PORT_SERVER="5000"
API_NAME = "Sustainable Development Goals API"
APP_VERSION = "1.0"

APP_PATH = "/home/cair0n/Documents/Projets/SDG/SDG_API/"
DATA_PATH = APP_PATH + "app/services/data/data.csv"

class DevelopmentConfig:
    DEBUG = True
    # SWAGGER Configuration
    SWAGGER_URL = '/api/docs'
    DATA_SWAGGER = 'http://127.0.0.1:5000/swagger'

class ProductionConfig:
    DEBUG = False
    # SWAGGER Configuration
    SWAGGER_URL = '/api/docs'
    DATA_SWAGGER = 'http://' + PRODUCTION_SERVER + ':' + PORT_SERVER + '/swagger'
