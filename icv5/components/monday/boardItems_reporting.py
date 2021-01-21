from icv5.components.monday import boardItem, column_keys, boardItems_inventory


class ReportingWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj, blank_item=False):

        new_column_dictionary = column_keys.reporting_wrapper

        super().__init__()

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**new_column_dictionary, **parent_obj.column_dictionary}
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):

        return self


class InventoryMovementItem(ReportingWrapper):

    column_dictionary = column_keys.inventory_movement

    def __init__(self, item_id=None, blank_item=True):
        if item_id:
            super().__init__(item_id, self)

        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

    def remove_stock(self):

        try:
            quantity = int(self.quantity.easy)
        except ValueError:
            quantity = 0

        new_quantity = quantity - 1

        self.quantity_before.change_value(quantity)
        self.quantity_after.change_value(new_quantity)

        self.adjust_parts_item(new_quantity)

        self.apply_column_changes()

    def adjust_parts_item(self, new_quantity):

        parts_item = boardItems_inventory.InventoryPartItem(self.partboard_id.easy)

        parts_item.quantity.change_value(new_quantity)

        parts_item.apply_column_changes()
