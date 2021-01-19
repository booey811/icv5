import os
from pprint import pprint

from icv5.components.monday import columns
from icv5.components.monday import exceptions
from icv5.components.monday.manage import manager
import settings


class MondayWrapper:
    column_type_dictionary = {
        'status': columns.StatusValue,
        'text': columns.TextValue,
        'number': columns.NumberValue,
        'dropdown': columns.DropdownValue,
        'date': columns.DateValue,
        'check': columns.CheckboxValue,
        'link': columns.LinkValue,
        'connect': columns.ConnectValue,
        'subitem': columns.SubitemValue
    }

    def __init__(self):
        self.cli_client = manager.create_client()
        self.id = None
        self.item = None
        self.name = None
        self.user_id = None
        self.adjusted_values = {}
        self.inventory_items = []

        if os.environ['DEBUG'] == 'console':
            self.debug = True

    def set_client_and_item(self, board_item_object, item_id):
        for pulse in self.cli_client.get_items(ids=[item_id], limit=1):
            board_item_object.item = pulse
            board_item_object.item.get_column_values()
            board_item_object.name = pulse.name.replace('"', ' Inch')
            board_item_object.id = pulse.id

    def set_attributes(self, board_item_object, column_dictionary):
        for attribute in column_dictionary:
            setattr(board_item_object, attribute, None)
            if board_item_object.item:
                for column in board_item_object.item.column_values:
                    if column.id == column_dictionary[attribute]['column_id']:
                        setattr(
                            board_item_object,
                            attribute,
                            self.column_type_dictionary[column_dictionary[attribute]['type']](
                                self,
                                attribute,
                                column
                            )
                        )
            else:
                setattr(board_item_object,
                        attribute,
                        self.column_type_dictionary[column_dictionary[attribute]['type']](
                            self,
                            attribute,
                            column_dictionary[attribute]['column_id']
                        )
                        )

    def apply_column_changes(self, verbose=False):
        if not self.adjusted_values:
            print('No changes detected')
            return False
        if self.item and not verbose:
            self.item.change_multiple_column_values(self.adjusted_values)
        elif self.item and verbose:
            for item in self.adjusted_values:
                print('{}: {}'.format(item, self.adjusted_values[item]))
                self.item.change_multiple_column_values({item: str(self.adjusted_values[item])})
        else:
            print('repair object has no item (has been created from within program)')
