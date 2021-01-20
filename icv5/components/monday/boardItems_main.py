import moncli

from icv5.components.monday import boardItem, exceptions, column_keys, manage, boardItems_inventory


class MainBoardWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj_columns, blank_item=False):

        new_column_dictionary = column_keys.main_wrapper

        super().__init__()

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**new_column_dictionary, **parent_obj_columns}
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):
        return self


# noinspection PyUnresolvedReferences
class MainBoardItem(MainBoardWrapper):
    column_dictionary = column_keys.main_item

    def __init__(self, item_id=None, blank_item=True):
        if item_id:
            super().__init__(item_id, self.column_dictionary)
        elif blank_item:
            super().__init__(None, self.column_dictionary, blank_item=True)
        else:
            raise exceptions.BoardItemArgumentError

    def create_inventory_info(self):
        ids = []
        names = []
        for repair in self.repairs.ids:
            ids.append('{}-{}-{}'.format(self.device.ids[0], repair, self.colour.index))

        for repair in self.repairs.easy:
            names.append('{} {} {}'.format(self.device.easy[0], repair, self.colour.easy))

        return {'ids': ids, 'names': names}

    def create_product_item(self, part_id, name):

        new_product_item = boardItems_inventory.InventoryProductItem()

        new_product_item.combined_id.change_value(part_id)
        new_product_item.device_id.change_value(str(self.device.ids[0]))
        new_product_item.repair_id.change_value(str(self.repairs.ids[count]))
        new_product_item.colour_id.change_value(str(self.colour.index))
        new_product_item.colour.change_value(str(self.colour.easy))
        new_product_item.device_label.change_value(str(self.device.easy[0]))
        new_product_item.repair_label.change_value(str(self.repairs.easy[count]))
        new_product_item.colour_label.change_value(str(self.colour.easy))

        created_item = manage.Manager().get_board('inventory_products').add_item(
            item_name=name,
            column_values=new_product_item.adjusted_values
        )

        return created_item

    def create_product_subitem(self, part_id, name, repair_id, repair_label, parent_item=None):
        parent = None
        if not parent_item:
            for item in self.cli_client.get_items(ids=[985573124], limit=1):
                parent = item
        else:
            parent = parent_item

        new_sub_item = boardItems_inventory.InventoryProductSubItem()

        new_sub_item.combined_id.change_value(part_id)
        new_sub_item.device_id.change_value(str(self.device.ids[0]))
        new_sub_item.repair_id.change_value(str(repair_id))
        new_sub_item.colour_id.change_value(str(self.colour.index))
        new_sub_item.colour.change_value(str(self.colour.easy))
        new_sub_item.device_label.change_value(str(self.device.easy[0]))
        new_sub_item.repair_label.change_value(str(repair_label))
        new_sub_item.colour_label.change_value(str(self.colour.easy))
        if parent:
            new_sub_item.parent_id.change_value(str(parent.id))

        board_item = parent.create_subitem(
            item_name=name,
            column_values=new_sub_item.adjusted_values
        )

        return board_item

    def create_log_item(self, product_item):

        # new_log_item = boardItems_inventory.InventoryLogItem()
        # new_log_item.combined_id.change_value(str(product_item.combined_id))
        # new_log_item.device_id.change_value(str(product_item.device_id))
        # new_log_item.repair_id.change_value(str(product_item.repair_id))
        # new_log_item.colour_id.change_value(str(product_item.colour_id))
        # new_log_item.colour.change_value(str(product_item.colour))
        # new_log_item.device_label.change_value(str(product_item.device_label))
        # new_log_item.repair_label.change_value(str(product_item.repair_label))
        # new_log_item.colour_label.change_value(str(product_item.colour_label))

        created_item = manage.Manager().get_board('inventory_logging').add_item(
            item_name=product_item.name
        )

        tester = boardItems_inventory.InventoryLogItem(created_item.id)
        tester.combined_id.change_value(str(product_item.combined_id.easy))
        tester.device_id.change_value(str(product_item.device_id.easy))
        tester.repair_id.change_value(str(product_item.repair_id.easy))
        tester.colour_id.change_value(str(product_item.colour_id.easy))
        # tester.colour.change_value(str(product_item.colour.easy))
        tester.device_label.change_value(str(product_item.device_label.easy))
        tester.repair_label.change_value(str(product_item.repair_label.easy))
        tester.colour_label.change_value(str(product_item.colour_label.easy))

        tester.apply_column_changes(verbose=True)

        return created_item

    def create_inventory_log(self):
        count = 0
        info = self.create_inventory_info()

        for part_id in info['ids']:

            results = manage.Manager().search_board(
                board_id='985542500',
                column_type='text',
                column_id=boardItems_inventory.InventoryProductSubItem.column_dictionary['combined_id']['column_id'],
                value=str(part_id)
            )

            if len(results) == 0:

                product_subitem = self.create_product_subitem(
                    part_id,
                    info['names'][count],
                    self.repairs.ids[count],
                    self.repairs.easy[count]
                )

            elif len(results) == 1:
                product_subitem = results[0:1][0]
                print(product_subitem)

            else:
                print('MainBoardItem.create_inventory_log else route')
                return False

            # noinspection PyTypeChecker
            self.create_log_item(boardItems_inventory.InventoryProductSubItem(product_subitem.id))

            count += 1


test = MainBoardItem(984662235)

test.create_inventory_log()
