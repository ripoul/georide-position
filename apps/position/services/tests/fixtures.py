from ..client import GeorideClient


class GeorideMixin(object):
    def any_token(self, user=None):
        user = user or GeorideClient().user
        token = user.driver.get_new_token()
        return token
