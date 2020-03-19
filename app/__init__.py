from flask import Flask, jsonify
from flask_restful import Api
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

# Declare the flask app and wrap it in Api
app = Flask(__name__)
api = Api(app)

from app import config
from app import routes

# Define the environment status
if config.env == 'DEVELOPMENT':
    conf = config.DevelopmentConfig
else:
    conf = config.ProductionConfig

app.config.from_object(conf)
app.config['BUNDLE_ERRORS'] = True

# Define the route where swagger will find the data to generate /api/docs
@app.route("/swagger")
def swaggerController():
    # Spec file for marshmallow
    swag = swagger(app)
    swag['info']['version'] = config.APP_VERSION
    swag['info']['title'] = config.API_NAME
    return jsonify(swag)

# Define the blueprint of the API
swaggerui_blueprint = get_swaggerui_blueprint(
    conf.SWAGGER_URL, # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    conf.DATA_SWAGGER,
    config = {  # Swagger UI config overrides
        'app_name': config.API_NAME
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix=conf.SWAGGER_URL)
