import boardItem
import boardItems_refurbs


class MainBoardWrapper(boardItem.MondayWrapper):

    boardItem_conversions = {
        'refurb_top_level': boardItems_refurbs.RefurbWrapper
    }

    def __init__(self, item_id=False, convert_to=False):
        if item_id:
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
                    'column_id': 'repair_complete',
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
                }
            }
            super().__init__()
            self.set_attributes(self, new_column_dictionary)
            if item_id:
                self.set_client_and_item(self, item_id)
        if convert_to:
            self.create_blank_item(convert_to)
        else:
            print('Else route')

    def create_blank_item(self, board):

        return self.boardItem_conversions[board]()







class MainBoardItem(MainBoardWrapper):

    def __init__(self, item_id):
        super().__init__(item_id)
