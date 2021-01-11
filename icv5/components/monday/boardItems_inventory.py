from icv5.components.monday import boardItem


class InventoryWrapper(boardItem.MondayWrapper):

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


class InventoryStockItem(InventoryWrapper):
    column_dictionary = {
        'sku': {
            'column_id': 'better_sku',
            'type': 'text'
        },
        'model': {
            'column_id': 'type',
            'type': 'text'
        },
        'category': {
            'column_id': 'status',
            'type': 'status'
        },
        'type': {
            'column_id': 'status6',
            'type': 'status'
        },
        'stock_level': {
            'column_id': 'inventory_oc_walk_in',
            'type': 'number'
        },
        'tracking': {
            'column_id': 'text',
            'type': 'text'
        },
        'vend_product_id': {
            'column_id': 'id',
            'type': 'text'
        },
        'stock_status': {
            'column_id': 'status5',
            'type': 'status'
        }
    }

    def __init__(self, item_id=False, blank_item=False):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class InventoryMappingItem(InventoryWrapper):

    column_dictionary = {
        'device_id': {
            'column_id': 'numbers3',
            'type': 'number'
        },
        'repair_id': {
            'column_id': 'device',
            'type': 'number'
        },
        'colour_id': {
            'column_id': 'numbers44',
            'type': 'number'
        },
        'vend_product_id': {
            'column_id': 'text',
            'type': 'text'
        },
        'sku': {
            'column_id': 'text0',
            'type': 'text'
        },
        'category': {
            'column_id': 'status43',
            'type': 'status'
        },
        'model': {
            'column_id': 'type',
            'type': 'text'
        },
        'type': {
            'column_id': 'status_11',
            'type': 'status'
        },
        'retail_price': {
            'column_id': 'retail_price',
            'type': 'number'
        },
        'supply_price': {
            'column_id': 'supply_price',
            'type': 'number'
        },
        'supply_glass_only': {
            'column_id': 'numbers7',
            'type': 'number'
        },
        'supply_glass_touch': {
            'column_id': 'numbers1',
            'type': 'number'
        },
        'supply_glass_touch_lcd': {
            'column_id': 'numbers_17',
            'type': 'number'
        },
        'parent_item': {
            'column_id': 'text1',
            'type': 'text'
        }
    }

    def __init__(self, item_id=False, blank_item=False):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class InventoryOrderItem(InventoryWrapper):
    column_dictionary = {
        'parent_item': {
            'column_id': 'parent_item__stock__1',
            'type': 'connect'
        },
        'status': {
            'column_id': 'status5',
            'type': 'status'
        }
    }

    def __init__(self, item_id=None, blank_item=False):
        if item_id:
            super().__init__(item_id, self)

        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class InventoryScreenRefurbItem(InventoryWrapper):
    column_dictionary = {
        'sku': {
            'column_id': 'text',
            'type': 'text'
        },
        'refurb_quantity': {
            'column_id': 'numbers',
            'type': 'number'
        },
    }

    def __init__(self, item_id=False, blank_item=False):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

