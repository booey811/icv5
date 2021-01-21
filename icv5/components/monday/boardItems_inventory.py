from icv5.components.monday import boardItem, column_keys, manage


class InventoryWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj, blank_item=False):

        new_column_dictionary = column_keys.inventory_wrapper

        super().__init__()

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**new_column_dictionary, **parent_obj.column_dictionary}
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):

        return self


class InventoryProductItem(InventoryWrapper):
    column_dictionary = column_keys.inventory_product

    def __init__(self, item_id=None, blank_item=True):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

class InventoryProductSubItem(InventoryWrapper):

    column_dictionary = column_keys.inventory_product_sub

    def __init__(self, item_id=None, blank_item=True):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

    def get_parent_item(self):
        for pulse in self.cli_client.get_items(ids=[self.parent_id.easy], limit=1):
            return pulse


class InventoryLogItem(InventoryWrapper):
    column_dictionary = column_keys.inventory_log

    def __init__(self, item_id=None, blank_item=True):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

# class InventoryStockItem(InventoryWrapper):
#
#     column_dictionary = column_keys.inventory_stock
#
#     def __init__(self, item_id=False, blank_item=False):
#         if item_id:
#             super().__init__(item_id, self)
#         elif blank_item:
#             super().__init__(None, self, blank_item=blank_item)
#
#
# class InventoryMappingItem(InventoryWrapper):
#
#     column_dictionary = column_keys.inventory_mapping
#
#     def __init__(self, item_id=False, blank_item=False):
#         if item_id:
#             super().__init__(item_id, self)
#         elif blank_item:
#             super().__init__(None, self, blank_item=blank_item)
#
#
# class InventoryOrderItem(InventoryWrapper):
#
#     column_dictionary = column_keys.inventory_order
#
#     def __init__(self, item_id=None, blank_item=False):
#         if item_id:
#             super().__init__(item_id, self)
#
#         elif blank_item:
#             super().__init__(None, self, blank_item=blank_item)
#
#
# class InventoryScreenRefurbItem(InventoryWrapper):
#
#     column_dictionary = column_keys.inventory_screenrefurb
#
#     def __init__(self, item_id=False, blank_item=False):
#         if item_id:
#             super().__init__(item_id, self)
#         elif blank_item:
#             super().__init__(None, self, blank_item=blank_item)
#

