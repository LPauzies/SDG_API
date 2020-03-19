from flask import request
from flask_restful import Resource, abort

from typing import Dict, Any

from app.services.SDGService import abort_if_country_doesnot_exist

class SDGByCountryResource(Resource):

    def get(self, country: str) -> Dict[str, Any]:
        """
        Get the 17 Sustainable Development Goals for a selected country
        ---
        tags:
            - Sustainable Development Goals API
        parameters:
            - in: path
              name: country
              description: The country to get the SDG from
              required: true
              type: string
        responses:
            200:
                description: JSON representing 17 SDG for the country
            404:
                description: The todo does not exist
        """
