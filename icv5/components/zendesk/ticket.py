import os

import zenpy
from zenpy.lib.api_objects import User, Ticket, Comment

import settings
from icv5.components.zendesk import exceptions
from icv5.components.zendesk.assets import ticket_descriptions


class ZendeskWrapper:

    def __init__(self):
        self.client = self.create_client()

    @staticmethod
    def create_client():
        client = zenpy.Zenpy(
            email='admin@icorrect.co.uk',
            token=os.environ["ZENDESKADMIN"],
            subdomain="icorrect"
        )
        return client


class ZendeskSearch(ZendeskWrapper):

    def __init__(self):
        super().__init__()

        self.client = self.create_client()

    def search_user_by_email(self, query_object):
        search = self.client.search(user=query_object.email.easy)
        if len(search) == 1:
            for item in search:
                return item

        elif len(search) > 1:
            raise exceptions.TooManyResultsFromUserEmail(query_object.email.easy)

        elif len(search) < 1:
            raise exceptions.ZeroResultsFromUserEmail(query_object.email.easy)

    def create_user(self, query_object):
        if query_object.phone.easy:
            user = User(name=query_object.name, email=query_object.email.easy, phone=query_object.phone.easy)
        else:
            user = User(name=query_object.name, email=query_object.email.easy)
        return self.client.users.create(user)

    def check_user_details(self, user, query_object):

        if not user.phone and query_object.phone.easy:
            print('adding phone to zen')
            user.phone = query_object.phone.easy
            self.client.users.update(user)

    def create_ticket_enquiry(self, query_object, description):
        try:
            user = self.search_user_by_email(query_object)
            self.check_user_details(user, query_object)
        except exceptions.TooManyResultsFromUserEmail:
            return False
        except exceptions.ZeroResultsFromUserEmail:
            user = self.create_user(query_object)
        ticket = Ticket(
            requester_id=user.id,
            subject='Your Enquiry with iCorrect',
            description=str(ticket_descriptions.added_to_enquiries_board(description))
        )
        ticket.comment = Comment(
            body="""Name: {}
            Enquiry: {}
            Email: {}
            Phone: {}
            """.format(
                query_object.name,
                description,
                query_object.email.easy,
                query_object.phone.easy
            ),
            public=False
        )
        return self.client.tickets.create(ticket)
