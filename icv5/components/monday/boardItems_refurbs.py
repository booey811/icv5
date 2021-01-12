from icv5.components.monday import boardItem, column_keys


class RefurbWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj, blank_item=False):

        new_column_dictionary = column_keys.refurb_wrapper

        super().__init__()

        self.top_level = None
        self.purchasing = None
        self.received = None
        self.tested = None
        self.repairing = None
        self.selling = None
        self.final_stats = None
        self.returns = None
        self.backlog = None

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**new_column_dictionary, **parent_obj.column_dictionary}
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):

        return self


class RefurbTopLevelBoardItem(RefurbWrapper):

    column_dictionary = column_keys.refurb_toplevel

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbPurchasingItem(RefurbWrapper):

    column_dictionary = column_keys.refurb_purchasing

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbReceivedItem(RefurbWrapper):

    column_dictionary = column_keys.refurb_received

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbTestedItem(RefurbWrapper):

    column_dictionary = column_keys.refurb_tested

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbRepairingItem(RefurbWrapper):

    column_dictionary = column_keys.refurb_repairing

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbSellingItem(RefurbWrapper):

    column_dictionary = column_keys.refurb_selling

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbFinalItem(RefurbWrapper):

    column_dictionary = column_keys.refurb_final

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbReturnItem(RefurbWrapper):

    column_dictionary = column_keys.refurb_return

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbBacklogItem(RefurbWrapper):

    column_dictionary = column_keys.refurb_backlog

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


