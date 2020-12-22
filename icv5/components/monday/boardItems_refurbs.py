import boardItem
import boardItems_main

class RefurbWrapper(boardItem.MondayWrapper):

    boardItem_conversions = {
        'refurb_top_level': boardItems_main.MainBoardWrapper
    }



    def __init__(self, item_id=False, convert_to=False):
        new_column_dictionary = {
            'unit_code': {
                'column_id': 'text4',
                'type': 'text'
            },
            'imei_sn': {
                'column_id': 'text',
                'type': 'text'
            },
            'batch_code': {
                'column_id': 'text0',
                'type': 'text'
            }
        }
        super().__init__()
        if item_id:
            self.set_client_and_item(self, item_id)
            self.set_attributes(self, new_column_dictionary)
        elif convert_to:
            self.create_blank_item(convert_to)
        else:print('else route')



    def create_blank_item(self, board):
        return self.boardItem_conversions[board]()

class TopLevelBoardItem(RefurbWrapper):
    column_dictionary = {
        'bought': {
            'column_id': 'status5',
            'type': 'status'
        },
        'received': {
            'column_id': 'bought_',
            'type': 'status'
        },
        'tested': {
            'column_id': 'received_',
            'type': 'status'
        },
        'repairing': {
            'column_id': 'tested_',
            'type': 'status'
        },
        'postchecks': {
            'column_id': 'repairing_',
            'type': 'status'
        },
        'forsale': {
            'column_id': 'post_checks_',
            'type': 'status'
        },
        'shipped': {
            'column_id': 'selling_',
            'type': 'status'
        },
        'delivered': {
            'column_id': 'status6',
            'type': 'status'
        },
    }

    def __init__(self, item_id):
        super().__init__(item_id)
        self.set_attributes(self, self.column_dictionary)



