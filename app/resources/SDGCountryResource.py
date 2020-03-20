from flask import request
from flask_restful import Resource, abort

from typing import Dict, Any

from app.services.SDGFilteringService import get_countries
from app.services.SDGOutputFormatterService import sdg_formatter_countries

from app.services.SDGFilteringService import SDGFilteringException

class SDGCountryResource(Resource):

    def get(self) -> Dict[str, Any]:
        """
        Get the countries and their country code available in the API
        ---
        tags:
            - Getting specific data
        responses:
            200:
                description: JSON containing the countries and their code
            503:
                description: The server encouters a problem while loading the data, service is unavailable
        """
        try:
            return {
                    "message" : "Success",
                    "status" : 200,
                    "data" : sdg_formatter_countries(get_countries())
                }, 200
        except OSError as e:
            abort(503, message=str(e), status=503)
