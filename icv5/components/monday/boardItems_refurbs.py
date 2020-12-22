from icv5.components.monday import boardItem


class RefurbWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj_columns, blank_item=False):

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
            },
            'test_status_column': {
                'column_id': 'status3',
                'type': 'status'
            }
        }

        super().__init__()

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**new_column_dictionary, **parent_obj_columns}
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item(blank_item)

    def create_blank_item(self):

        return self


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

    def __init__(self, item_id=False, blank_item=False):
        if item_id:
            super().__init__(item_id, self.column_dictionary)
        elif blank_item:
            super().__init__(None, self.column_dictionary, blank_item=blank_item)


