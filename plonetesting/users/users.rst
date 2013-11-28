Settings of this package
------------------------

Instalation of this product adds *email as login feature*.

    >>> browser = self.browser
    >>> browser.open("http://nohost/plone/login_form")
    >>> 'E-mail' in self.browser.contents
    True


Register new user
-----------------

Let's logil as portal owner

    >>> from Products.PloneTestCase.PloneTestCase import portal_owner, default_password
    >>> browser.open('http://nohost/plone/login_form')
    >>> browser.getControl('E-mail').value = portal_owner
    >>> browser.getControl('Password').value = default_password
    >>> browser.getControl('Log in').click()

Let's add new user

    >>> browser.open('http://nohost/plone/@@usergroup-userprefs')
    >>> browser.getControl('Add New User').click()
    >>> '@@new-user' in browser.url
    True


    Fill out the form. We use the same full name as before, to test
    that we get a different user id.
    >>> browser.getControl('Full Name').value = 'Bob Jones'
    >>> browser.getControl('E-mail').value = 'bob-jones@example.com'
    >>> browser.getControl('Password').value = 'secret'
    >>> browser.getControl('Confirm password').value = 'secret'

Our profile shoud have additional fields, let's fill them too

    >>> browser.getControl('Function').value = 'Bob\'s function'
    >>> browser.getControl('Company name').value = 'Bob\'s company'

    >>> browser.getControl('Company logo').value = 'http://plone.org/logo.png'
    >>> browser.getControl('Personal picture').value = 'http://plone.org/logo.png'

    >>> browser.getControl('Quote').value = 'Bob\'s quote'
    >>> browser.getControl('Summary').value = 'Bob\'s summary'

#TODO: add test - Social media links (social media icons (twitter, linkedin) with link

    >>> browser.getControl('Specialities').value = 'Bob\'s specialities'

    >>> browser.getControl('Register').click()

    We can really get the new user.

    >>> browser.getControl('Show all').click()
    >>> browser.getLink(url='bob-jones').click()
    >>> '@@user-information?userid=bob-jones' in browser.url
    True


Obtain user data from linkedin
------------------------------

Check control panel with linkedin settings

    >>> browser.open('http://nohost/plone/@@linkedin-settings')
    >>> 'Linkedin settings' in self.browser.contents
    True

    Let's try submit empty form

    >>> browser.open('http://nohost/plone/@@linkedin-settings')
    >>> browser.getControl('Save').click()
    >>> 'There were some errors.' in self.browser.contents
    True

    Let's try submit filled form

    >>> browser.getControl('API key').value = 'ApIkEy'
    >>> browser.getControl('Secret key').value = 'sEcReTkEy'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved.' in self.browser.contents
    True
    >>> browser.open('http://nohost/plone/@@linkedin-settings')
    >>> 'ApIkEy' in self.browser.contents
    True
    >>> 'sEcReTkEy' in self.browser.contents
    True


    Let's try cancel filled form
    >>> browser.open('http://nohost/plone/@@linkedin-settings')
    >>> browser.getControl('API key').value = 'ApIkEyNeW'
    >>> browser.getControl('Secret key').value = 'sEcReTkEyNeW'
    >>> browser.getControl('Cancel').click()
    >>> 'Edit cancelled.' in self.browser.contents
    True
    >>> browser.open('http://nohost/plone/@@linkedin-settings')
    >>> 'ApIkEyNeW' in self.browser.contents
    False
    >>> 'sEcReTkEyNeW' in self.browser.contents
    False

Check *Import Data from LinkeIn* on profile page

    Login as a Bob
    >>> browser.open('http://nohost/plone/logout')
    >>> browser.open('http://nohost/plone/login_form')
    >>> browser.getControl('E-mail').value = 'bob-jones@example.com'
    >>> browser.getControl('Password').value = 'secret'
    >>> browser.getControl('Log in').click()
    >>> browser.open('http://nohost/plone/@@personal-information')
    >>> 'Import Data from LinkeIn' in self.browser.contents
    True
    >>> browser.getControl('Import Data from LinkeIn').click()
    >>> "Data from Linkedin is imported" in self.browser.contents
    True
    >>> browser.getControl('Save').click()
    >>> 'Changes saved.' in self.browser.contents
    True
    >>> browser.open('http://nohost/plone/@@personal-information')
    >>> browser.getControl('Cancel').click()
    >>> 'Changes canceled.' in self.browser.contents
    True
