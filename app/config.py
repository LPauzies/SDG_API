env = "DEVELOPMENT"
PRODUCTION_SERVER= "172.17.4.154" # Un exemple
PORT_SERVER="5000"
API_NAME = "Sustainable Development Goals API"
APP_VERSION = "1.0"

DATA_ABSOLUTE_PATH = "/home/cair0n/Documents/Projets/SDG_API/app/data/data.csv"
DATA_PROJECT_PATH = "SDG_API/app/data/data.csv"

class BaseConfig:
    DEBUG = True

class DevelopmentConfig(BaseConfig):
    # SWAGGER Configuration
    SWAGGER_URL = '/api/docs'
    DATA_SWAGGER = 'http://127.0.0.1:5000/swagger'

class ProductionConfig(BaseConfig):
    DEBUG = False
    # SWAGGER Configuration
    SWAGGER_URL = '/api/docs'
    DATA_SWAGGER = 'http://' + PRODUCTION_SERVER + ':' + PORT_SERVER + '/swagger'
