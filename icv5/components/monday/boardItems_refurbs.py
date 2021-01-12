from icv5.components.monday import boardItem


class RefurbWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj, blank_item=False):

        new_column_dictionary = {
        }

        super().__init__()

        self.top_level = None
        self.purchasing = None
        self.received = None
        self.tested = None
        self.repairing = None
        self.selling = None
        self.final_stats = None
        self.returns = None
        self.backlog = None

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
        },
        'unit_code': {
            'column_id': 'unit_code',
            'type': 'text'
        },
        'imei_sn': {
            'column_id': 'imei',
            'type': 'text'
        },
        'batch_code': {
            'column_id': 'batch_code',
            'type': 'text'
        }
    }

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbReceivedItem(RefurbWrapper):
    column_dictionary = {
        'phonecheck': {
            'column_id': 'status',
            'type': 'status'
        },
        'imei_sn': {
            'column_id': 'text',
            'type': 'text'
        },
        'batch_code': {
            'column_id': 'text8',
            'type': 'text'
        },
        'unit_code': {
            'column_id': 'text6',
            'type': 'text'
        },
        'face_id': {
            'column_id': 'status5',
            'type': 'status'
        },
        'battery': {
            'column_id': 'face_id',
            'type': 'status'
        },
        'screen': {
            'column_id': 'battery',
            'type': 'status'
        },
        'rear_glass': {
            'column_id': 'front_screen',
            'type': 'status'
        },
        'microphone': {
            'column_id': 'rear_glass',
            'type': 'status'
        },
        'charging_port': {
            'column_id': 'microphone',
            'type': 'status'
        },
        'wireless': {
            'column_id': 'charging_port',
            'type': 'status'
        },
        'mute_vol': {
            'column_id': 'wireless',
            'type': 'status'
        },
        'power': {
            'column_id': 'mute_vol_buttons',
            'type': 'status'
        },
        'earpiece': {
            'column_id': 'power_button',
            'type': 'status'
        },
        'loudspeaker': {
            'column_id': 'earpiece_mesh',
            'type': 'status'
        },
        'wifi': {
            'column_id': 'loudspeaker',
            'type': 'status'
        },
        'bluetooth': {
            'column_id': 'wifi',
            'type': 'status'
        },
        'rear_cam': {
            'column_id': 'bluetooth',
            'type': 'status'
        },
        'rear_lens': {
            'column_id': 'rear_camera',
            'type': 'status'
        },
        'front_camera': {
            'column_id': 'rear_lens',
            'type': 'status'
        },
        'siri': {
            'column_id': 'front_camera',
            'type': 'status'
        },
        'nfc': {
            'column_id': 'siri',
            'type': 'status'
        },
        'batt_health': {
            'column_id': 'numbers',
            'type': 'number'
        }
    }

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbTestedItem(RefurbWrapper):
    column_dictionary = {
    }

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbRepairingItem(RefurbWrapper):
    column_dictionary = {

    }

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbSellingItem(RefurbWrapper):
    column_dictionary = {
    }

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbFinalItem(RefurbWrapper):
    column_dictionary = {
    }

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbReturnItem(RefurbWrapper):
    column_dictionary = {
    }

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbBacklogItem(RefurbWrapper):
    column_dictionary = {
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
