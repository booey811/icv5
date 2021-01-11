import os

import moncli
from moncli.api_v2 import exceptions as moncli_except

import settings
from icv5.components.monday import exceptions


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
        }
    }

    board_ids = {
        'main': '349212843',
        'stock': '867934405',
        'inventory_mappings': '868065293',
        'stock_levels': '867934405',
        'refurb_toplevel': '925661179',
        'refurb_purchasing': '952635143',
        'refurb_received': '925661892',
        'refurb_tested': '925877501',
        'refurb_repairing': '925662587',
        'refurb_selling': '925662877',
        'refurb_backlog': '925663181',
        'refurb_returns': '925663428',
        'backmarket_refs': '928091586'
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
        try:
            board = client.get_board(self.board_ids[board_name])
        except moncli_except.MondayApiError:
            raise exceptions.NoBoardFound(self.board_ids[board_name], board_name)
        return board

    @staticmethod
    def compare_repair_objects(object_to_change, object_to_read, attributes_dictionary):
        ignore_list = ['adjusted_values']
        copy_list = ['client', 'debug']
        for item in attributes_dictionary:

            if item in ignore_list:
                continue

            if item in copy_list:
                setattr(object_to_change, item, getattr(object_to_read, item))
                continue

            if item in object_to_change.__dict__:

                object_value = getattr(object_to_change, item)
                replacement_value = attributes_dictionary[item]

                if not object_value and replacement_value:
                    # No ori value, write replacement value
                    result = replacement_value

                elif object_value and replacement_value:
                    # Both values present, overwrite ori value with new value
                    result = replacement_value

                elif object_value and not replacement_value:
                    # No replacement available - skip change
                    return False

                elif not object_value and not replacement_value:
                    # No values available - skip change
                    return False

                else:
                    print('else route')
                    return False

                to_change = getattr(object_to_change, item)

                if to_change:
                    to_change.change_value(result)

    @staticmethod
    def get_attribute_list(custom_object):
        dicts = custom_object.__dict__
        ignore_list = ['item']
        result = {}
        for item in dicts:
            if item not in ignore_list:
                result[item] = dicts[item]

        return result

    def add_update(self, item_object, user_id=False, client=False, update=False, status=False, notify=False):
        # Select Client (Which User Will be posting updates/notifications)
        """Adds updates or notifies monday users, with options to adjust statuses

        Args:
            monday_id (int): ID of the Monday ite mthat the update will be centered around
            user (str): Name of the user and client to be used to post the update/notification
            update (bool, optional): Provide the text of the update required. Defaults to False.
            status (list[2], optional): List containing the ID of the status column to be changed and the label to be changed to. Defaults to False.
            notify (list[2], optional): Contains text for the notification to be sent and the ID of the user to send it to. Defaults to False.
            non_main (bool, optional): [description]. Defaults to False.

        Returns:
            False: No item could be found for the provided ID
        """
        client = self.create_client(client)
        # Post Update, if provided
        if update:
            item_object.add_update(body=update)
        # Change Status, if provided
        # if status:
        #     # Ensure 'status' is a 2 length list
        #     if len(status) == 2:
        #         item.change_column_value(column_id=status[0], column_value={"label": status[1]})
        #     else:
        #         print("status list has not been provided correctly")
        # Send Notification, if requested
        if notify:
            # Check 'notify' is a 2 length list
            if len(notify) == 2:
                client.create_notification(
                    text=notify[0],
                    user_id=notify[1],
                    target_id=item_object.id,
                    target_type=moncli.NotificationTargetType.Project
                )
            else:
                print("notify list has not been provided correctly")



manager = Manager()
