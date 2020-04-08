from app import api

from app.resources.SDGCountryResource import SDGCountryResource
from app.resources.SDGGoalsResource import SDGGoalsResource

from app.resources.SDGByCountryResource import SDGByCountryResource
from app.resources.SDGByCountryCodeResource import SDGByCountryCodeResource
from app.resources.SDGByCountryCodeGoalsResource import SDGByCountryCodeGoalsResource
from app.resources.SDGByTopicCodeResource import SDGByTopicCodeResource

api.add_resource(SDGCountryResource, '/api/sdg/countries')
api.add_resource(SDGGoalsResource, '/api/sdg/goals')

api.add_resource(SDGByTopicCodeResource, '/api/sdg/topic/<string:topic>')

api.add_resource(SDGByCountryResource, '/api/sdg/country/<string:country>')
api.add_resource(SDGByCountryCodeResource, '/api/sdg/countrycode/<string:country_code>')

api.add_resource(SDGByCountryCodeGoalsResource, '/api/sdg/<string:country_code>/<string:topic>')
