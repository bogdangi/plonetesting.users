from linkedin import linkedin
from plonetesting.users.linkedincontrolpanel.interfaces import ILinkedinSettins
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class LinkedinUtility(object):
    """ Linkedin utility """

    autentification = None
    return_url = ''

    def setReturnURL(self, url):
        """ set return URL """
        self.return_url = url

    def getAutentification(self):
        """ return autentification """
        # Get data from Linkedin control panel
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ILinkedinSettins)
        API_KEY = settings.api_key
        API_SECRET = settings.secret_key
        RETURN_URL = self.return_url
        self.autentification = linkedin.LinkedInAuthentication(
            API_KEY, API_SECRET, RETURN_URL,
            # request all avaliable data from user, but unfortunatelly it gives
            # just basic data
            # TODO: check what is wrong
            linkedin.PERMISSIONS.enums.values())
        return self.autentification

    def getUserProfile(self, code):
        """ return user profile """
        application = linkedin.LinkedInApplication(self.autentification)
        self.autentification.authorization_code = code
        self.autentification.get_access_token()
        return application.get_profile()
