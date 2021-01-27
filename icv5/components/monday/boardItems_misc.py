from icv5.components.monday import boardItem, column_keys, exceptions



class EnquiryWrapper(boardItem.MondayWrapper):

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


class GeneralEnquiryItem(EnquiryWrapper):

    column_dictionary = column_keys.enquiries_general

    def __init__(self, item_id=None, blank_item=True):
        if item_id:
            super().__init__(item_id, self)
            assert getattr(self, 'email'), NoEmailOnMonday(self)
            if not self.body.easy:
                self.body.easy = 'This Enquiry Is Blank On Monday'

        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class NoEmailOnMonday(Exception):

    def __init__(self, general_enquiry_item):
        print('No Email On Monday Which is Required To Process This Enquiry\n{}\n{}'.format(
            general_enquiry_item.name,
            general_enquiry_item.id
        ))
