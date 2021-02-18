from icv5.components.monday import manage

class TooManyResultsFromUserEmail(Exception):

    def __init__(self, mainBoard_object, email):
        print('While Searching Zendesk With A User=email@email.com Query, Too Many Results Were Returned\n{}'.format(
            email))
        manage.Manager().add_update(
            mainBoard_object,
            update="Too Many Users found with email: {}\n\nCannot create zendesk ticket".format(email)
        )


class ZeroResultsFromUserEmail(Exception):

    def __init__(self, email):
        print('While Searching Zendesk With A User=email@email.com Query, No Results Were Returned\n{}'.format(
            email))


class UserAlreadyExists(Exception):

    def __init__(self, email):
        print('You Are Trying To Create a User That Already Exists with email: {}'.format(email))


class CannotConvertAttributeToCustomField(Exception):

    def __init__(self, attribute):

        print('Cannot Find {} attribute in zendesk.custom_fields.ids_to_attributes'.format(attribute))