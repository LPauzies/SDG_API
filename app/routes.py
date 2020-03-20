from app import api

from app.resources.SDGCountryResource import SDGCountryResource
from app.resources.SDGGoalsResource import SDGGoalsResource

from app.resources.SDGByCountryResource import SDGByCountryResource
from app.resources.SDGByCountryCodeResource import SDGByCountryCodeResource

api.add_resource(SDGCountryResource, '/api/sdg/countries')
api.add_resource(SDGGoalsResource, '/api/sdg/goals')

api.add_resource(SDGByCountryResource, '/api/sdg/<string:country>')
api.add_resource(SDGByCountryCodeResource, '/api/sdg/<int:country_code>')
