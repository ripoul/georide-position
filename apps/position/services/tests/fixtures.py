from ..client import GeorideClient

class GeorideMixin(object):
    def any_token(self, user=None):
        user = user or GeorideClient().user
        token = geo.getNewToken(user.email, user.password)
        return token
