class Customer:
    def __init__(self, forename='', surname='', email='', password='', is_agb=False, is_newsletter=False):
        self.forename = forename
        self.surname = surname
        self.email = email
        self.password = password
        self.is_agb = is_agb
        self.is_newsletter = is_newsletter
