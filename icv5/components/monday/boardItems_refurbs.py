from icv5.components.monday import boardItem


class RefurbWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj, blank_item=False):

        new_column_dictionary = {
        }

        super().__init__()

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**new_column_dictionary, **parent_obj.column_dictionary}
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):

        return self


class RefurbTopLevelBoardItem(RefurbWrapper):
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
        'purchasing_item': {
            'column_id': 'connect_boards5',
            'type': 'connect'
        },
        'received_item': {
            'column_id': 'received__beta__1',
            'type': 'connect'
        },
        'tested_item': {
            'column_id': 'connect_boards_1',
            'type': 'connect'
        },
        'repairs_item': {
            'column_id': 'connect_boards_2',
            'type': 'connect'
        },
        'sales_item': {
            'column_id': 'connect_boards4',
            'type': 'connect'
        }
    }

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbPurchasingItem(RefurbWrapper):
    column_dictionary = {

    }

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)
