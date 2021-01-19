class TooManyResultsFromUserEmail(Exception):

    def __init__(self, email):
        print('While Searching Zendesk With A User=email@email.com Query, Too Many Results Were Returned\n{}'.format(
            email))


class ZeroResultsFromUserEmail(Exception):

    def __init__(self, email):
        print('While Searching Zendesk With A User=email@email.com Query, No Results Were Returned\n{}'.format(
            email))


class UserAlreadyExists(Exception):

    def __init__(self, email):
        print('YOu Are Trying To Create a User That Already Exists with email: {}'.format(email))
