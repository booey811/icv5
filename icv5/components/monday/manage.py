import os

import moncli
import settings


class Manager:
    client_credentials = {
        'system': {
            'v1': os.environ['MONV1SYS'],
            'v2': os.environ['MONV2SYS'],
            'user_name': 'systems@icorrect.co.uk',
            'user_id': 12304876
        },

        'emails': {
            'v1': os.environ['MONV1EML'],
            'v2': os.environ['MONV2EML'],
            'user_name': 'icorrectltd@gmail.com',
            'user_id': 15365289
        },

        'error': {
            'v1': os.environ['MONV1ERR'],
            'v2': os.environ['MONV2ERR'],
            'user_name': 'admin@icorrect.co.uk',
            'user_id': 15365289
        },

    }

    board_ids = {
        'main': '349212843',
        'stock': '867934405',
        'mappings': '14028101',
        'refurb_toplevel': '925661179'
    }

    def __init__(self):
        pass

    def create_client(self, client_name=False):
        if not client_name:
            client_name = 'system'

        client = moncli.MondayClient(
            user_name=self.client_credentials[client_name]['user_name'],
            api_key_v1=self.client_credentials[client_name]['v1'],
            api_key_v2=self.client_credentials[client_name]['v2']
        )

        return client

    def get_board(self, board_name, client_name=False):
        client = self.create_client(client_name=client_name)

        board = client.get_board_by_id(self.board_ids[board_name])

        return board


manager = Manager()
