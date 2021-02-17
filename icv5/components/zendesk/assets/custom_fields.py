from zenpy.lib.api_objects import CustomField


class ZendeskCustomFieldWrapper:

    def __init__(self, ticket_object, custom_field_dict):
        self.ticket_object = ticket_object
        self.id = custom_field_dict['id']
        self.value = custom_field_dict['value']

    def adjust_value(self, value):
        if isinstance(value, str):
            value = [value]
        for item in value:
            self.ticket_object.ticket.custom_fields.append(
                CustomField(
                    id=self.id,
                    value=item
                )
            )


class ZendeskCustomTextField(ZendeskCustomFieldWrapper):

    def __init__(self, ticket_object, custom_field_dict):
        super().__init__()

        self.ticket_object = ticket_object
        self.custom_field = custom_field_dict
        self.value = custom_field_dict['value']

    def change_value(self, text_to_add):
        self.ticket_object.ticket.custom_fields.append(CustomField(
            id=self.custom_field.id,
            value=str(text_to_add)
        ))


class ZendeskCustomDropdownField(ZendeskCustomFieldWrapper):

    def __init__(self, ticket_object, custom_field):
        super().__init__()

        self.ticket_object = ticket_object
        self.custom_field = custom_field

        self.associated_tag = custom_field.value

    def change_value(self, tag_to_add=None, remove=False):

        if remove:
            self.ticket_object.remove_tag(remove)
        elif tag_to_add:
            self.ticket_object.add_tag(tag_to_add)
        else:
            print('ZendeskCustomDropdownField change_value else route')


class ZendeskCustomCheckboxField(ZendeskCustomFieldWrapper):

    def __init__(self, ticket_object, custom_field):
        super().__init__()

        self.ticket_object = ticket_object
        self.custom_field = custom_field

        self.value = self.custom_field.value

    def change_value(self, settings_option):
        if not settings_option:
            self.custom_field.value = False
        elif settings_option:
            self.custom_field.value = True


ids_to_attributes = {
    360004242638: {
        'attribute': 'imei_sn',
        'type': ZendeskCustomTextField
    },
    360004570218: {
        'attribute': 'main_id',
        'type': ZendeskCustomTextField
    },
    360005102118: {
        'attribute': 'passcode',
        'type': ZendeskCustomTextField
    },
    360005728837: {
        'attribute': 'repair_status',
        'type': ZendeskCustomDropdownField
    },
    360006582758: {
        'attribute': 'postcode',
        'type': ZendeskCustomTextField
    },
    360006582778: {
        'attribute': 'street_address',
        'type': ZendeskCustomTextField
    },
    360006582798: {
        'attribute': 'flat_number',
        'type': ZendeskCustomTextField
    },
    360006704157: {
        'attribute': 'tracking_url',
        'type': ZendeskCustomTextField
    },
    360008818998: {
        'attribute': 'device_type',
        'type': ZendeskCustomDropdownField
    },
    360010430958: {
        'attribute': 'on_main',
        'type': ZendeskCustomCheckboxField
    },
    360012686858: {
        'attribute': 'enquiry_id',
        'type': ZendeskCustomTextField
    },
    360010444117: {
        'attribute': 'service_type',
        'type': ZendeskCustomDropdownField
    },
    360010408778: {
        'attribute': 'client_type',
        'type': ZendeskCustomDropdownField
    }
}
