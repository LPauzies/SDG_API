from flask import request
from flask_restful import Resource, abort

from typing import Dict, Any

from app.services.SDGFilteringService import get_topic_data
from app.services.SDGOutputFormatterService import sdg_formatter_topic_data

from app.services.SDGFilteringService import SDGFilteringException

class SDGByTopicCodeResource(Resource):

    def get(self, topic: str) -> Dict[str, Any]:
        """
        Get the main stats of a topic
        ---
        tags:
            - Getting complete data for corresponding topic
        parameters:
            - in: path
              name: topic
              description: The topic to get data from
              required: true
              type: string
        responses:
            200:
                description: JSON containing the stats of the topic
            404:
                description: The topic code has not been found
            503:
                description: The server encouters a problem while loading the data, service is unavailable
        """
        try:
            return {
                    "message" : "Success",
                    "status" : 200,
                    "data" : sdg_formatter_topic_data(get_topic_data(topic.upper()))
                }, 200
        except OSError as e:
            abort(503, message=str(e), status=503)
        except SDGFilteringException as e:
            abort(404, message=str(e), status=404)
