from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema
from zope.interface import implements
from zope import schema
from plonetesting.users import _


class IEnhancedUserDataSchema(IUserDataSchema):
    """
    Use all the fields from the default user data schema, and add various
    extra fields.
    """

    function = schema.TextLine(
        title=_(u'function', default=u'Function'),
        description=_(u'help_function',
                      default=u"Fill in which function you work with."),
        required=False,
    )

    company_name = schema.TextLine(
        title=_(u'company_name', default=u'Company name'),
        description=_(u'help_company_name',
                      default=u"Fill in which company you work in."),
        required=False,
    )

    company_logo = schema._field.URI(
        title=_(u'company_logo', default=u"Company logo"),
        description=_(u'help_company_logo',
                      default=u"URL to your company logo image"),
        required=False,
    )

    personal_picture = schema._field.URI(
        title=_(u'personal_picture', default=u"Personal picture"),
        description=_(u'help_personal_picture',
                      default=u"URL to your personal picture image"),
        required=False,
    )

    quote = schema.Text(
        title=_(u'quote', default=u'Quote'),
        description=_(u'help_quote',
                      default=u"Fill in your quote."),
        required=False,
    )

    summary = schema.Text(
        title=_(u'summary', default=u'Summary'),
        description=_(u'help_summary',
                      default=u"Fill in your summary."),
        required=False,
    )

    social_links = schema.List(
        title=_(u'social_links', default=u'Social links'),
        description=_(u'help_social_links',
                      default=u"Fill your social media links."),
        required=False,
        unique=True,
        value_type=schema._field.URI(
            title=_(u'social_link', default=u"Social link")),
    )

    specialities = schema.Text(
        title=_(u'specialities', default=u'Specialities'),
        description=_(u'help_specialities',
                      default=u"Fill in your specialities."),
        required=False,
    )


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        return IEnhancedUserDataSchema
