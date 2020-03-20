from flask import request
from flask_restful import Resource, abort

from typing import Dict, Any

from app.services.SDGFilteringService import get_data_from_one_country
from app.services.SDGOutputFormatterService import sdg_formatter

from app.services.SDGFilteringService import SDGFilteringException

class SDGByCountryResource(Resource):

    def get(self, country: str) -> Dict[str, Any]:
        """
        Get the Sustainable Development Goals data for a selected country
        ---
        tags:
            - Getting complete data for corresponding country
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
                description: The country has not been found
            503:
                description: The server encouters a problem while loading the data, service is unavailable
        """
        try:
            return {
                    "message" : "Success",
                    "status" : 200,
                    "data" : sdg_formatter(get_data_from_one_country(country.upper()))
                }, 200
        except OSError as e:
            abort(503, message=str(e), status=503)
        except SDGFilteringException as e:
            abort(404, message=str(e), status=404)
