from plone.app.registry.browser import controlpanel
from z3c.form import button
from Products.statusmessages.interfaces import IStatusMessage

from plonetesting.users import _
from plonetesting.users.linkedincontrolpanel.interfaces import ILinkedinSettins


class LinkedinEditForm(controlpanel.RegistryEditForm):

    schema = ILinkedinSettins
    label = _(u"Linkedin settings")
    description = _(u"""Settings for linkedin application""")

    def updateFields(self):
        super(LinkedinEditForm, self).updateFields()

    def updateWidgets(self):
        super(LinkedinEditForm, self).updateWidgets()

    @button.buttonAndHandler(_(u"Save"), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(
            _(u"Changes saved."), "info")
        self.request.response.redirect(
            "%s/%s" % (self.context.absolute_url(), self.control_panel_view))

    @button.buttonAndHandler(_(u"Cancel"), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
            _(u"Edit cancelled."), "info")
        self.request.response.redirect(
            "%s/%s" % (self.context.absolute_url(), self.control_panel_view))


class LinkedinSettinsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = LinkedinEditForm
