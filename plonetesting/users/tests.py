import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc

from Products.PloneTestCase.PloneTestCase import FunctionalTestCase

from Acquisition import aq_base
from zope.component import getSiteManager
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

# BBB Zope 2.12
try:
    from Testing.testbrowser import Browser
except ImportError:
    from Products.Five.testbrowser import Browser

from Products.PluggableAuthService.interfaces.plugins import IValidationPlugin
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
from plonetesting.users.interfaces import ILinkedinUtility

ptc.setupPloneSite(products=['plonetesting.users'])


class LinkedinUtilityTest(object):
    """ Linkedin utility """

    autentification = None
    return_url = ''

    def setReturnURL(self, url):
        """ set return URL """
        self.return_url = url

    def getAutentification(self):
        """ return autentification """
        class Authorization(object):
            authorization_url = ''

        autentification = Authorization()
        autentification.authorization_url = self.return_url + '&code=code'
        self.autentification = autentification
        return self.autentification

    def getUserProfile(self, code):
        """ return user profile """
        return {
            'firstName': 'FirstName',
            'lastName': 'LastName',
            'headline': 'Function name'}


class TestCase(FunctionalTestCase):

    def afterSetUp(self):
        super(TestCase, self).afterSetUp()
        self.browser = Browser()
        self.portal.acl_users._doAddUser('admin', 'secret', ['Manager'], [])
        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = mailhost = MockMailHost('MailHost')
        self.membership = self.portal.portal_membership
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)
        sm.unregisterUtility(provided=ILinkedinUtility)
        sm.registerUtility(
            factory=LinkedinUtilityTest, provided=ILinkedinUtility)

    def beforeTearDown(self):
        self.portal.MailHost = self.portal._original_MailHost
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(
            aq_base(self.portal._original_MailHost),
            provided=IMailHost)

        portal = getUtility(ISiteRoot)
        pas_instance = portal.acl_users
        plugin = getattr(pas_instance, 'test', None)
        if plugin is not None:
            plugins = pas_instance._getOb('plugins')
            plugins.deactivatePlugin(IValidationPlugin, 'test')
            #plugins.deactivatePlugin(IPropertiesPlugin, 'test')
            pas_instance.manage_delObjects('test')

    def setMailHost(self):
        self.portal.MailHost.smtp_host = 'localhost'
        setattr(self.portal, 'email_from_address', 'admin@foo.com')

    def unsetMailHost(self):
        self.portal.MailHost.smtp_host = ''
        setattr(self.portal, 'email_from_address', '')


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='plonetesting.users',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='plonetesting.users.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='plonetesting.users',
        #    test_class=TestCase),

        ztc.FunctionalDocFileSuite(
            'users.rst', package='plonetesting.users',
            test_class=TestCase),

    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
