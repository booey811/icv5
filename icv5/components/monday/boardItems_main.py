from icv5.components.monday import boardItem, exceptions


class MainBoardWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj_columns, blank_item=False):

        new_column_dictionary = {

            'address1': {
                'column_id': 'passcode',
                'type': 'text'
            },
            'address2': {
                'column_id': 'dup__of_passcode',
                'type': 'text'
            },
            'company_name': {
                'column_id': 'text15',
                'type': 'text'
            },
            'date_collected': {
                'column_id': 'date3',
                'type': 'date'
            },
            'date_received': {
                'column_id': 'date4',
                'type': 'date'
            },
            'date_repaired': {
                'column_id': 'collection_date',
                'type': 'date'
            },
            'booking_date': {
                'column_id': 'date6',
                'type': 'date'
            },
            'deadline_date': {
                'column_id': 'date36',
                'type': 'date'
            },
            'deactivate': {
                'column_id': 'check71',
                'type': 'check'
            },
            'email': {
                'column_id': 'text5',
                'type': 'text'
            },
            'imei_sn': {
                'column_id': 'text4',
                'type': 'text'
            },
            'invoiced': {
                'column_id': 'check',
                'type': 'check'
            },
            'client': {
                'column_id': 'status',
                'type': 'status'
            },
            'colour': {
                'column_id': 'status8',
                'type': 'status'
            },
            'data': {
                'column_id': 'status55',
                'type': 'status'
            },
            'device': {
                'column_id': 'device0',
                'type': 'dropdown'
            },
            'eod': {
                'column_id': 'blocker',
                'type': 'status'
            },
            'has_case': {
                'column_id': 'status_14',
                'type': 'status'
            },
            'notifications': {
                'column_id': 'dropdown8',
                'type': 'dropdown'
            },
            'refurb': {
                'column_id': 'status_15',
                'type': 'status'
            },
            'repairs': {
                'column_id': 'repair',
                'type': 'dropdown'
            },
            'screen_condition': {
                'column_id': 'screen_condition',
                'type': 'dropdown'
            },
            'service': {
                'column_id': 'service',
                'type': 'status'
            },
            'status': {
                'column_id': 'status4',
                'type': 'status'
            },
            'type': {
                'column_id': 'status24',
                'type': 'status'
            },
            'zenlink': {
                'column_id': 'status5',
                'type': 'status'
            },
            'new_eod': {
                'column_id': 'status_17',
                'type': 'status'
            },
            'number': {
                'column_id': 'text00',
                'type': 'text'
            },
            'passcode': {
                'column_id': 'text8',
                'type': 'text'
            },
            'postcode': {
                'column_id': 'text93',
                'type': 'text'
            },
            'v_id': {
                'column_id': 'text88',
                'type': 'text'
            },
            'z_ticket_id': {
                'column_id': 'text6',
                'type': 'text'
            },
            'zendesk_url': {
                'column_id': 'link1',
                'type': 'link'
            },
            'test_status_column': {
                'column_id': 'status_10',
                'type': 'status'
            }
        }

        super().__init__()

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**new_column_dictionary, **parent_obj_columns}
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):
        return self


class MainBoardItem(MainBoardWrapper):
    column_dictionary = {
    }

    def __init__(self, item_id=None, blank_item=True):
        if item_id:
            super().__init__(item_id, self.column_dictionary)
        elif blank_item:
            super().__init__(None, self.column_dictionary, blank_item=True)
        else:
            raise exceptions.BoardItemArgumentError


