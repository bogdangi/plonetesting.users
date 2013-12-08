from zope.interface import Interface


class ILinkedinUtility(Interface):
    """ Linkedin utility """

    def setReturnURL(url):
        """ set return URL """

    def getAutentification():
        """ return autentification """

    def getUserProfile():
        """ return user profile """
