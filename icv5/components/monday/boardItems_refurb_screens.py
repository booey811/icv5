from icv5.components.monday import boardItem, column_keys


class ScreenRefurbWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj, blank_item=False):

        new_column_dictionary = column_keys.screen_refurb_wrapper

        super().__init__()

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**new_column_dictionary, **parent_obj.column_dictionary}
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):

        return self


class ScreenRefurbItem(ScreenRefurbWrapper):

    column_dictionary = column_keys.screen_refurb_item

    def __init__(self, item_id=None, blank_item=True):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

        self.sub_items = []

    def get_subitems(self):
        for item in self.sub_item_ids.easy:
            self.sub_items.append(ScreenRefurbSubItem(item))


class ScreenRefurbSubItem(ScreenRefurbWrapper):

    column_dictionary = column_keys.screen_refurb_sub_item

    def __init__(self, item_id=None, blank_item=True):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

