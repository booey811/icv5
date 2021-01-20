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
            ids.append('{} {} {}'.format(self.device.ids[0], repair, self.colour.index))

        for repair in self.repairs.easy:
            names.append('{} {} {}'.format(self.device.easy[0], repair, self.colour.easy))

        return {'ids': ids, 'names': names}

    def create_inventory_log(self):
        count = 0
        info = self.create_inventory_info()
        stock_board = self.cli_client.get_board(manage.Manager.board_ids['stock_new'])

        for part_id in info['ids']:
            col_val = moncli.entities.create_column_value(
                id=boardItems_inventory.InventoryLogItem.column_dictionary['combined_id']['column_id'],
                column_type=moncli.ColumnType.text,
                text=part_id
            )

            results = stock_board.get_items_by_column_values(col_val)

            if len(results) == 0:

                new_stock = boardItems_inventory.InventoryLogItem()
                new_stock.combined_id.change_value(part_id)

                stock_board.add_item(item_name=info['names'][count], column_values=new_stock.adjusted_values)

                print('creating product')

            for item in results:
                print(item.__dict__)

            count += 1


test = MainBoardItem(983544514)

test.create_inventory_log()

