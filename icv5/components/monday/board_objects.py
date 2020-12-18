import moncli

class MondayWrapper:

    def __init__(self):
        pass

    def set_item(self, item_id):
        for pulse in board_object.get_items(ids=[item_id], limit=1):
            self.item = pulse
            self.name = pulse.name.replace('"', ' Inch')

    def set_attributes(self, columns_list):
        for column in columns_list:
            pass




class MainBoard(MondayWrapper):

    def __init__(self, item_id):
        self.set_item(item_id)

