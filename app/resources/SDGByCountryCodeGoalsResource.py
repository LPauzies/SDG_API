from flask import request
from flask_restful import Resource, abort

from typing import Dict, Any

from app.services.SDGFilteringService import get_topic_from_one_country
from app.services.SDGOutputFormatterService import sdg_formatter_goal_country

from app.services.SDGFilteringService import SDGFilteringException

class SDGByCountryCodeGoalsResource(Resource):

    def get(self, country_code: int, topic: str) -> Dict[str, Any]:
        """
        Get the Sustainable Development Goals topic data for a selected country code
        ---
        tags:
            - Getting topic data for corresponding country
        parameters:
            - in: path
              name: country_code
              description: The country code to get the SDG from
              required: true
              type: integer
            - in: path
              name: topic
              description: The topic to retrieve the data from
              required: true
              type: string
        responses:
            200:
                description: JSON representing 17 SDG for the country code
            404:
                description: The country code has not been found / The topic has not been found
            503:
                description: The server encouters a problem while loading the data, service is unavailable
        """
        try:
            return {
                    "message" : "Success",
                    "status" : 200,
                    "data" : sdg_formatter_goal_country(get_topic_from_one_country(country_code, topic.upper()))
                }, 200
        except OSError as e:
            abort(503, message=str(e), status=503)
        except SDGFilteringException as e:
            abort(404, message=str(e), status=404)
