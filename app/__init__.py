from flask import Flask, jsonify
from flask_restful import Api
from flask_swagger import swagger
from flask_cors import CORS

# Declare the flask app and wrap it in Api
app = Flask(__name__)
api = Api(app)
CORS(app, resources={"/api/sdg/*": {"origins":"*"}})

from app import config
from app import routes

# Define the route where swagger will find the data to generate /api/docs
@app.route("/swagger")
def swaggerController():
    # Spec file for marshmallow
    swag = swagger(app)
    swag['info']['version'] = config.APP_VERSION
    swag['info']['title'] = config.API_NAME
    return jsonify(swag)
