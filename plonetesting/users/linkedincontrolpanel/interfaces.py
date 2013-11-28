from zope import schema
from zope.interface import Interface

from plonetesting.users import _


class ILinkedinSettins(Interface):
    """Global linkedin settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    api_key = schema.TextLine(
        title=_(u"API key"),
        required=True,
        default=u'',
    )
    secret_key = schema.TextLine(
        title=_(u"Secret key"),
        required=True,
        default=u'',
    )
