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

    def create_inventory_log(self):
        count = 0
        info = self.create_inventory_info()
        stock_board = self.cli_client.get_board(manage.Manager.board_ids['inventory_products'])

        for part_id in info['ids']:

            results = manage.Manager().search_board(
                'inventory_products',
                'text',
                boardItems_inventory.InventoryLogItem.column_dictionary['combined_id']['column_id'],
                str(part_id)
            )

            if len(results) == 0:

                new_item = boardItems_inventory.InventoryLogItem()



                new_item.combined_id.change_value(part_id)
                new_item.device_id.change_value(str(self.device.ids[0]))
                new_item.repair_id.change_value(str(self.repairs.ids[count]))
                new_item.colour_id.change_value(str(self.colour.index))
                new_item.colour.change_value(str(self.colour.easy))
                new_item.device_label.change_value(str(self.device.easy[0]))
                new_item.repair_label.change_value(str(self.repairs.easy[count]))
                new_item.colour_label.change_value(str(self.colour.easy))

                mon_item = stock_board.add_item(item_name=info['names'][count], column_values=new_item.adjusted_values)

                return mon_item

            elif len(results) == 1:

                print('Product Found')

            count += 1

