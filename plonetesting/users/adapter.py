from plone.app.users.browser.personalpreferences import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):

    def get_company_name(self):
        return self.context.getProperty('company_name', '')

    def set_company_name(self, value):
        self.context.setMemberProperties({'company_name': value or ''})

    company_name = property(get_company_name, set_company_name)

    def get_function(self):
        return self.context.getProperty('function', '')

    def set_function(self, value):
        self.context.setMemberProperties({'function': value or ''})

    function = property(get_function, set_function)

    def get_company_logo(self):
        return self.context.getProperty('company_logo', '')

    def set_company_logo(self, value):
        return self.context.setMemberProperties({'company_logo': value})

    company_logo = property(get_company_logo, set_company_logo)

    def get_personal_picture(self):
        return self.context.getProperty('personal_picture', '')

    def set_personal_picture(self, value):
        return self.context.setMemberProperties({'personal_picture': value})

    personal_picture = property(get_personal_picture, set_personal_picture)

    def get_quote(self):
        return self.context.getProperty('quote', '')

    def set_quote(self, value):
        self.context.setMemberProperties({'quote': value or ''})

    quote = property(get_quote, set_quote)

    def get_summary(self):
        return self.context.getProperty('summary', '')

    def set_summary(self, value):
        self.context.setMemberProperties({'summary': value or ''})

    summary = property(get_summary, set_summary)

    def get_social_links(self):
        return self.context.getProperty('social_links', [])

    def set_social_links(self, value):
        return self.context.setMemberProperties({'social_links': value})

    social_links = property(get_social_links, set_social_links)

    def get_specialities(self):
        return self.context.getProperty('specialities', '')

    def set_specialities(self, value):
        self.context.setMemberProperties({'specialities': value or ''})

    specialities = property(get_specialities, set_specialities)
