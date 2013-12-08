from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema
from zope.interface import implements
from zope import schema
from zope.formlib import form

from zope.event import notify
from plone.app.form.validators import null_validator
from plone.app.controlpanel.events import ConfigurationChangedEvent
from plone.protect import CheckAuthenticator
from plonetesting.users.interfaces import ILinkedinUtility
from zope.component import getUtility


from Products.statusmessages.interfaces import IStatusMessage


from plone.app.users.browser.personalpreferences import UserDataPanel

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


class CustomizedUserDataPanel(UserDataPanel):

    @form.action(_(u'label_save', default=u'Save'), name=u'save')
    def handle_edit_action(self, action, data):
        CheckAuthenticator(self.request)

        if form.applyChanges(self.context, self.form_fields, data,
                             self.adapters):
            IStatusMessage(self.request).addStatusMessage(
                _("Changes saved."), type="info")
            notify(ConfigurationChangedEvent(self, data))
            self._on_save(data)
        else:
            IStatusMessage(self.request).addStatusMessage(
                _("No changes made."), type="info")

    @form.action(_(u'label_cancel', default=u'Cancel'),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        IStatusMessage(self.request).addStatusMessage(_("Changes canceled."),
                                                      type="info")

        self.request.response.redirect(self.request['ACTUAL_URL'])
        return ''

    @form.action(_(u'Import Data from LinkeIn'),
                 name=u'import_data_from_linkedin')
    def import_data_from_linkedin(self, action, data):

        linkedin_utility = getUtility(ILinkedinUtility)
        # this is a marker which helps to identify that it comes from linkedin
        linkedin_utility.setReturnURL(
            self.request['ACTUAL_URL'] + '?import_data_from_linkedin=true')

        return self.request.response.redirect(
            linkedin_utility.getAutentification().authorization_url)

    def __call__(self):
        super(CustomizedUserDataPanel, self).__call__()
        code = self.request.get('code', None)
        if code is not None and \
                self.request.get(
                    'import_data_from_linkedin', None) is not None:

            user_profile = getUtility(ILinkedinUtility).getUserProfile(code)

            data_from_linkedin = {
                'fullname': ' '.join(
                    [user_profile[i] for i in ['firstName', 'lastName']]),
                'function': user_profile['headline']}

            # Update widgets not form data
            for i in data_from_linkedin.keys():
                self.widgets[i].setRenderedValue(data_from_linkedin[i])

            self.form_reset = False

            data = {}
            errors, action = form.handleSubmit(
                self.actions, data, self.validate)
            # the following part will make sure that previous error not
            # get overriden by new errors. This is usefull for subforms. (ri)
            if self.errors is None:
                self.errors = errors
            else:
                if errors is not None:
                    self.errors += tuple(errors)

            if errors:
                self.status = _('There were errors')
                result = action.failure(data, errors)
            elif errors is not None:
                self.form_reset = True
                result = action.success(data)
            else:
                result = None

            self.form_result = result

            IStatusMessage(self.request).addStatusMessage(
                _(u"Data from Linkedin is imported. " +
                  "To apply this data just click button 'Save'"), type="info")

        return self.render()
