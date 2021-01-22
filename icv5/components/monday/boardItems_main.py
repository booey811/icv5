import time

import moncli

from icv5.components.monday import boardItem, exceptions, column_keys, manage, boardItems_inventory, \
    boardItems_reporting


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

        self.product_codes = {}

    def create_inventory_info(self):

        ids = []
        names = []
        colours = {
            'TrackPad',
            'Charging Port',
            'Headphone Jack',
            'Home Button',
            'Front Screen Universal',
            'Rear Glass',
            'Front Screen (LG)',
            'Front Screen (Tosh)'
        }

        id_count = 0
        for repair in self.repairs.ids:
            if self.repairs.labels[id_count] in colours:
                ids.append('{}-{}-{}'.format(self.device.ids[0], repair, self.colour.index))
            else:
                ids.append('{}-{}'.format(self.device.ids[0], repair, self.colour.index))
            id_count += 1

        name_count = 0
        for repair in self.repairs.easy:
            if self.repairs.labels[name_count] in colours:
                names.append('{} {} {}'.format(self.device.easy[0], repair, self.colour.easy))
            else:
                names.append('{} {}'.format(self.device.easy[0], repair))
            name_count += 1

        return {'ids': ids, 'names': names}

    def create_product_item(self, part_id, name, count):

        name = name.replace('"', ' Inch')
        new_product_item = boardItems_inventory.InventoryRepairItem()
        id_split = part_id.split('-')
        new_product_item.combined_id.change_value(part_id)
        new_product_item.device_id.change_value(str(id_split[0]))
        new_product_item.repair_id.change_value(str(id_split[1]))
        if len(id_split) == 3:
            new_product_item.colour_id.change_value(str(id_split[2]))
            new_product_item.colour_label.change_value(str(self.colour.easy))
            new_product_item.colour.change_value(str(self.colour.easy))
        new_product_item.device_label.change_value(str(self.device.easy[0]))
        new_product_item.repair_label.change_value(str(self.repairs.easy[count]))

        created_item = manage.Manager().get_board('inventory_products').add_item(
            item_name=name,
            column_values=new_product_item.adjusted_values
        )
        return created_item

    def create_inventory_log(self, log_type='main', financial_object=False, retry=False):

        count = 0
        info = self.create_inventory_info()

        for part_id in info['ids']:
            results = manage.Manager().search_board(
                board_id='984924063',
                column_type='text',
                column_id=boardItems_inventory.InventoryWrapper.new_column_dictionary['combined_id']['column_id'],
                value=str(part_id)
            )

            # No Results - Create A Product
            if len(results) == 0:
                new_product = boardItems_inventory.InventoryRepairItem(
                    self.create_product_item(part_id, info['names'][count], count).id
                )
                if log_type == 'main':
                    time.sleep(5)
                    repairboard_item = boardItems_inventory.InventoryRepairItem(new_product.id)
                    repairboard_item.complete.change_value('Trigger')
                    repairboard_item.apply_column_changes()
                    count += 1
                    continue
                elif log_type == 'financial' and financial_object:
                    financial_object.parts_status.change_value('Failed')
                    financial_object.subitems.delete_all_subitems()
                    raise exceptions.ProductBeingCreated(info['names'][count])

            # 1 Results - Check Out Stock
            elif len(results) == 1:
                for pulse in results:
                    repairboard_item = boardItems_inventory.InventoryRepairItem(pulse.id)
                    if log_type == 'financial' and financial_object:
                        subitem = boardItems_reporting.FinancialCreationSubItem()
                        if count > 0:
                            discounted = int(repairboard_item.sale_price.easy) - 10
                        else:
                            discounted = repairboard_item.sale_price.easy
                        subitem.change_multiple_attributes(
                            [
                                ['sale_price', repairboard_item.sale_price.easy],
                                ['supply_price', repairboard_item.supply_price.easy],
                                ['discounted_price', discounted],
                                ['quantity_used', 1]
                            ],
                            return_only=True
                        )
                        subitem.part_url.change_value(
                            text=repairboard_item.partboard_id.easy,
                            url='https://icorrect.monday.com/boards/985177480/pulses/{}'
                        )
                        new_subitem = financial_object.item.create_subitem(
                            item_name=repairboard_item.name,
                            column_values=subitem.adjusted_values
                        )
                        financial_object.parts_status.change_value('Complete')

                    else:
                        repairboard_item.complete.change_value('Trigger')
                        repairboard_item.apply_column_changes()

            else:
                print('MainBoardItem.create_inventory_log else route')

            count += 1

        if log_type == 'financial':
            return

        self.eod.change_value('Complete')
        self.add_to_finance.change_value('Do Now!')
        self.apply_column_changes()
