# Main Board Dictionaries
main_wrapper = {
    'address1': {
        'column_id': 'passcode',
        'type': 'text'
    },
    'address2': {
        'column_id': 'dup__of_passcode',
        'type': 'text'
    },
    'company_name': {
        'column_id': 'text15',
        'type': 'text'
    },
    'date_collected': {
        'column_id': 'date3',
        'type': 'date'
    },
    'date_received': {
        'column_id': 'date4',
        'type': 'date'
    },
    'date_repaired': {
        'column_id': 'collection_date',
        'type': 'date'
    },
    'booking_date': {
        'column_id': 'date6',
        'type': 'date'
    },
    'deadline_date': {
        'column_id': 'date36',
        'type': 'date'
    },
    'deactivate': {
        'column_id': 'check71',
        'type': 'check'
    },
    'email': {
        'column_id': 'text5',
        'type': 'text'
    },
    'phone': {
        'column_id': 'text00',
        'type': 'text'
    },
    'imei_sn': {
        'column_id': 'text4',
        'type': 'text'
    },
    'invoiced': {
        'column_id': 'check',
        'type': 'check'
    },
    'client': {
        'column_id': 'status',
        'type': 'status'
    },
    'colour': {
        'column_id': 'status8',
        'type': 'status'
    },
    'data': {
        'column_id': 'status55',
        'type': 'status'
    },
    'device': {
        'column_id': 'device0',
        'type': 'dropdown'
    },
    'eod': {
        'column_id': 'eod',
        'type': 'status'
    },
    'has_case': {
        'column_id': 'status_14',
        'type': 'status'
    },
    'notifications': {
        'column_id': 'dropdown8',
        'type': 'dropdown'
    },
    'parts_used': {
        'column_id': 'parts_used',
        'type': 'dropdown'
    },
    'refurb': {
        'column_id': 'status_15',
        'type': 'status'
    },
    'repairs': {
        'column_id': 'repair',
        'type': 'dropdown'
    },
    'screen_condition': {
        'column_id': 'screen_condition',
        'type': 'dropdown'
    },
    'service': {
        'column_id': 'service',
        'type': 'status'
    },
    'status': {
        'column_id': 'status4',
        'type': 'status'
    },
    'type': {
        'column_id': 'status24',
        'type': 'status'
    },
    'zenlink': {
        'column_id': 'status5',
        'type': 'status'
    },
    'new_eod': {
        'column_id': 'status_17',
        'type': 'status'
    },
    'number': {
        'column_id': 'text00',
        'type': 'text'
    },
    'passcode': {
        'column_id': 'text8',
        'type': 'text'
    },
    'postcode': {
        'column_id': 'text93',
        'type': 'text'
    },
    'v_id': {
        'column_id': 'text88',
        'type': 'text'
    },
    'zendesk_id': {
        'column_id': 'text6',
        'type': 'text'
    },
    'zendesk_url': {
        'column_id': 'link1',
        'type': 'link'
    },
    'test_trigger': {
        'column_id': 'status_111',
        'type': 'status'
    },
    'add_to_finance': {
        'column_id': 'add_to_finance8',
        'type': 'status'
    },
    'be_courier_collection': {
        'column_id': 'be_courier_collection',
        'type': 'status'
    },
    'be_courier_return': {
        'column_id': 'be_courier_return',
        'type': 'status'
    },
    'company': {
        'column_id': 'company',
        'type': 'text'
    },
    'be_stock_checker': {
        'column_id': 'be_stock_checker',
        'type': 'status'
    }
}

main_item = {}


# Inventory Dictionaries
inventory_wrapper = {
    'combined_id': {
        'column_id': 'combined_id',
        'type': 'text'
    },
    'colour': {
        'column_id': 'colour',
        'type': 'status'
    },
    'device_label': {
        'column_id': 'device_label',
        'type': 'text'
    },
    'repair_label': {
        'column_id': 'repair_label',
        'type': 'text'
    },
    'colour_label': {
        'column_id': 'colour_label',
        'type': 'text'
    },
    'device_id': {
        'column_id': 'device_id',
        'type': 'text'
    },
    'repair_id': {
        'column_id': 'repair_id',
        'type': 'text'
    },
    'colour_id': {
        'column_id': 'colour_id',
        'type': 'text'
    }
}

inventory_repair = {
    'complete': {
        'column_id': 'complete',
        'type': 'status'
    },
    'sale_price': {
        'column_id': 'sale_price',
        'type': 'readonly'
    },
    'supply_price': {
        'column_id': 'supply_price',
        'type': 'readonly'
    },
    'partboard_id': {
        'column_id': 'partboard_id',
        'type': 'readonly'
    },
    'quantity': {
        'column_id': 'quantity',
        'type': 'readonly'
    },
    'tracking': {
        'column_id': 'tracking',
        'type': 'status'
    },
    'dual_only_id': {
        'column_id': 'dual_only_id',
        'type': 'text'
    },
    'repair_credits': {
        'column_id': 'repair_credits',
        'type': 'number'
    },
    'glass': {
        'column_id': 'glass_only',
        'type': 'readonly'
    },
    'touch': {
        'column_id': 'glass___touch',
        'type': 'readonly'
    },
    'lcd': {
        'column_id': 'glass__touch___lcd',
        'type': 'readonly'
    }
}

inventory_part = {
    'quantity': {
        'column_id': 'quantity',
        'type': 'number'
    },
    'sale_price': {
        'column_id': 'sale_price',
        'type': 'number'
    },
    'supply_price': {
        'column_id': 'supply_price',
        'type': 'number'
    },
    'glass': {
        'column_id': 'glass_only',
        'type': 'number'
    },
    'touch': {
        'column_id': 'glass_touch',
        'type': 'number'
    },
    'lcd': {
        'column_id': 'glass_touch_lcd',
        'type': 'number'
    }
}

inventory_stock_count = {
    'count_quantity': {
        'column_id': 'count_quantity',
        'type': 'number'
    },
    'count_status': {
        'column_id': 'count_status',
        'type': 'status'
    },
    'parts_id': {
        'column_id': 'parts_id',
        'type': 'text'
    },
    'quantity_before': {
        'column_id': 'quantity_before',
        'type': 'number'
    },
    'current_quantity': {
        'column_id': 'current_quantity',
        'type': 'readonly'
    },
    'supply_price': {
        'column_id': 'supply_price3',
        'type': 'number'
    }
}

inventory_order = {
    'order_quantity': {
        'column_id': 'order_quantity',
        'type': 'number'
    },
    'order_status': {
        'column_id': 'order_status',
        'type': 'status'
    },
    'quantity_after': {
        'column_id': 'quantity_after',
        'type': 'number'
    },
    'quantity_received': {
        'column_id': 'quantity_received',
        'type': 'number'
    },
    'unit_cost': {
        'column_id': 'unit_cost',
        'type': 'number'
    },
    'parts_id': {
        'column_id': 'parts_id',
        'type': 'text'
    }
}


# Reporting Dictionaries
reporting_wrapper = {

}

reporting_financial = {
    'mainboard_id': {
        'column_id': 'mainboard_id6',
        'type': 'text'
    },
    'parts_status': {
        'column_id': 'parts_status',
        'type': 'status'
    },
    'subitems': {
        'column_id': 'subitems',
        'type': 'subitem'
    }
}

reporting_financial_sub = {
    'sale_price': {
        'column_id': 'sale_price',
        'type': 'number'
    },
    'supply_price': {
        'column_id': 'supply_price',
        'type': 'number'
    },
    'quantity_used': {
        'column_id': 'quantity_used',
        'type': 'number'
    },
    'discounted_price': {
        'column_id': 'discounted_price',
        'type': 'number'
    },
    'part_url': {
        'column_id': 'part_url',
        'type': 'link'
    },
    'movementboard_id': {
        'column_id': 'movementboard_id',
        'type': 'text'
    },
    'partboard_id': {
        'column_id': 'partboard_id',
        'type': 'text'
    }
}


# FinancialDictionaries
financial_wrapper = {

}

financial_item = {
    'mainboard_id': {
        'column_id': 'mainboard_id6',
        'type': 'text'
    },
    'parts_status': {
        'column_id': 'parts_status',
        'type': 'status'
    },
    'subitems': {
        'column_id': 'subitems',
        'type': 'subitem'
    },
    'be_generator': {
        'column_id': 'be_generator',
        'type': 'check'
    },
    'stock_adjustment': {
        'column_id': 'stock_adjustment',
        'type': 'status'
    },
    'repair_credits': {
        'column_id': 'repair_credits',
        'type': 'readonly'
    },
    'linked_client': {
        'column_id': 'client',
        'type': 'readonly'
    }
}

financial_mainlink = {
    'device': {
        'column_id': 'device0',
        'type': 'dropdown'
    },
    'repairs': {
        'column_id': 'repair',
        'type': 'dropdown'
    },
    'colour': {
        'column_id': 'status8',
        'type': 'status'
    },
    'refurb': {
        'column_id': 'status_15',
        'type': 'status'
    }
}

financial_subitem = {
    'sale_price': {
        'column_id': 'sale_price',
        'type': 'number'
    },
    'supply_price': {
        'column_id': 'supply_price',
        'type': 'number'
    },
    'quantity_used': {
        'column_id': 'quantity_used',
        'type': 'number'
    },
    'part_url': {
        'column_id': 'part_url',
        'type': 'link'
    },
    'movementboard_id': {
        'column_id': 'movementboard_id',
        'type': 'text'
    },
    'partboard_id': {
        'column_id': 'partboard_id',
        'type': 'text'
    },
    'eod_status': {
        'column_id': 'status2',
        'type': 'status'
    },
    'movement_url': {
        'column_id': 'movement_url',
        'type': 'link'
    },
    'repair_credits': {
        'column_id': 'repair_credits',
        'type': 'number'
    }
}

inventory_movement = {
    'quantity': {
        'column_id': 'quantity',
        'type': 'readonly'
    },
    'quantity_before': {
        'column_id': 'quantity_before',
        'type': 'number'
    },
    'quantity_after': {
        'column_id': 'quantity_after',
        'type': 'number'
    },
    'partboard_id': {
        'column_id': 'partboard_id',
        'type': 'readonly'
    },
    'date': {
        'column_id': 'date',
        'type': 'date'
    },
    'mainboard_name': {
        'column_id': 'mainboard_name',
        'type': 'text'
    },
    'mainboard_id': {
        'column_id': 'mainboard_id',
        'type': 'text'
    },
    'product_id': {
        'column_id': 'product_id',
        'type': 'text'
    },
    'movement_type': {
        'column_id': 'movement_type',
        'type': 'status'
    },
    'part_url': {
        'column_id': 'part_url',
        'type': 'link'
    },
    'device_label': {
        'column_id': 'device_label2',
        'type': 'text'
    },
    'colour_label': {
        'column_id': 'colour_label6',
        'type': 'text'
    },
    'repair_label': {
        'column_id': 'repair_label1',
        'type': 'text'
    },
    'device_id': {
        'column_id': 'device_id4',
        'type': 'text'
    },
    'repair_id': {
        'column_id': 'repair_id3',
        'type': 'text'
    },
    'colour_id': {
        'column_id': 'colour_id1',
        'type': 'text'
    }
}


# NEW Screen Refurb Dictionaries
screen_refurbs_wrapper = {
    'combined_id': {
        'column_id': 'combined_id',
        'type': 'text'
    },
    'device_id': {
        'column_id': 'device_id',
        'type': 'text'
    },
    'repair_id': {
        'column_id': 'repair_id',
        'type': 'text'
    },
    'colour_id': {
        'column_id': 'colour_id',
        'type': 'text'
    },
    'device_label': {
        'column_id': 'device_label',
        'type': 'text'
    },
    'repair_label': {
        'column_id': 'repair_label',
        'type': 'text'
    },
    'colour_label': {
        'column_id': 'colour_label',
        'type': 'text'
    },
    'part_id': {
        'column_id': 'part_id',
        'type': 'text'
    }
}

screen_refurbs_menu = {
    'refurbable_stock': {
        'column_id': 'refurbable_stock',
        'type': 'number'
    },
    'deglassed_stock': {
        'column_id': 'deglassed_stock',
        'type': 'number'
    }
}

screen_refurbs_ongoing = {
    'starting_quantity': {
        'column_id': 'starting_quantity',
        'type': 'number'
    },
    'lcd_damage': {
        'column_id': 'lcd_damage',
        'type': 'number'
    },
    're_runs': {
        'column_id': 're_runs',
        'type': 'number'
    },
    'refurb_part_id': {
        'column_id': 'refurb_part_id',
        'type': 'text'
    },
    'refurb_type': {
        'column_id': 'refurb_type',
        'type': 'status'
    }
}


# Screen Refurb Dictionaries
screen_refurb_wrapper = {

}

screen_refurb_item = {
    'sub_item_ids': {
        'column_id': 'subitems',
        'type': 'subitem'
    },
    'batch_code': {
        'column_id': 'batch_code',
        'type': 'text'
    },
    'batch_status': {
        'column_id': 'batch_status',
        'type': 'status'
    }
}

screen_refurb_sub_item = {
    'unit_code': {
        'column_id': 'unit_code',
        'type': 'text'
    },
    'ic': {
        'column_id': 'ic',
        'type': 'status'
    },
    'model': {
        'column_id': 'model',
        'type': 'status'
    },
    'refurb_type': {
        'column_id': 'refurb_type',
        'type': 'status'
    },
    'deglassing': {
        'column_id': 'deglassing',
        'type': 'status'
    },
    'glassing': {
        'column_id': 'glassing',
        'type': 'status'
    },
    'result': {
        'column_id': 'result',
        'type': 'status'
    },
    'complete': {
        'column_id': 'complete',
        'type': 'status'
    },
    'damage': {
        'column_id': 'damage',
        'type': 'status'
    },
    'final_refurb_type': {
        'column_id': 'final_refurb_type',
        'type': 'status'
    },

}


# Unit Refurbishment Dictionaries
refurb_wrapper = {}

refurb_toplevel = {
    'bought': {
        'column_id': 'status5',
        'type': 'status'
    },
    'received': {
        'column_id': 'bought_',
        'type': 'status'
    },
    'tested': {
        'column_id': 'received_',
        'type': 'status'
    },
    'repairing': {
        'column_id': 'tested_',
        'type': 'status'
    },
    'postchecks': {
        'column_id': 'repairing_',
        'type': 'status'
    },
    'forsale': {
        'column_id': 'post_checks_',
        'type': 'status'
    },
    'shipped': {
        'column_id': 'selling_',
        'type': 'status'
    },
    'delivered': {
        'column_id': 'status6',
        'type': 'status'
    },
    'purchasing_item': {
        'column_id': 'connect_boards5',
        'type': 'connect'
    },
    'received_item': {
        'column_id': 'received__beta__1',
        'type': 'connect'
    },
    'tested_item': {
        'column_id': 'connect_boards_1',
        'type': 'connect'
    },
    'repairs_item': {
        'column_id': 'connect_boards_2',
        'type': 'connect'
    },
    'sales_item': {
        'column_id': 'connect_boards4',
        'type': 'connect'
    },
    'unit_code': {
        'column_id': 'unit_code',
        'type': 'text'
    },
    'imei_sn': {
        'column_id': 'imei',
        'type': 'text'
    },
    'batch_code': {
        'column_id': 'batch_code',
        'type': 'text'
    }
}

refurb_purchasing = {}

refurb_received = {
    'phonecheck': {
        'column_id': 'status',
        'type': 'status'
    },
    'imei_sn': {
        'column_id': 'text',
        'type': 'text'
    },
    'batch_code': {
        'column_id': 'batch_code',
        'type': 'text'
    },
    'unit_code': {
        'column_id': 'unit_code',
        'type': 'text'
    },
    'face_id': {
        'column_id': 'status5',
        'type': 'status'
    },
    'battery': {
        'column_id': 'face_id',
        'type': 'status'
    },
    'screen': {
        'column_id': 'battery',
        'type': 'status'
    },
    'rear_glass': {
        'column_id': 'front_screen',
        'type': 'status'
    },
    'microphone': {
        'column_id': 'rear_glass',
        'type': 'status'
    },
    'charging_port': {
        'column_id': 'microphone',
        'type': 'status'
    },
    'wireless': {
        'column_id': 'charging_port',
        'type': 'status'
    },
    'mute_vol': {
        'column_id': 'wireless',
        'type': 'status'
    },
    'power': {
        'column_id': 'mute_vol_buttons',
        'type': 'status'
    },
    'earpiece': {
        'column_id': 'power_button',
        'type': 'status'
    },
    'loudspeaker': {
        'column_id': 'earpiece_mesh',
        'type': 'status'
    },
    'wifi': {
        'column_id': 'loudspeaker',
        'type': 'status'
    },
    'bluetooth': {
        'column_id': 'wifi',
        'type': 'status'
    },
    'rear_cam': {
        'column_id': 'bluetooth',
        'type': 'status'
    },
    'rear_lens': {
        'column_id': 'rear_camera',
        'type': 'status'
    },
    'front_cam': {
        'column_id': 'rear_lens',
        'type': 'status'
    },
    'siri': {
        'column_id': 'front_camera',
        'type': 'status'
    },
    'nfc': {
        'column_id': 'siri',
        'type': 'status'
    },
    'batt_health': {
        'column_id': 'numbers',
        'type': 'number'
    },
    'haptic': {
        'column_id': 'nfc',
        'type': 'status'
    }
}

refurb_tested = {
    'phonecheck': {
        'column_id': 'phonecheck',
        'type': 'status'
    },
    'imei_sn': {
        'column_id': 'imei',
        'type': 'text'
    },
    'batch_code': {
        'column_id': 'batch_code',
        'type': 'text'
    },
    'unit_code': {
        'column_id': 'unit_code',
        'type': 'text'
    },
    'face_id': {
        'column_id': 'face_id7',
        'type': 'status'
    },
    'battery': {
        'column_id': 'battery9',
        'type': 'status'
    },
    'screen': {
        'column_id': 'battery',
        'type': 'status'
    },
    'rear_glass': {
        'column_id': 'front_screen',
        'type': 'status'
    },
    'microphone': {
        'column_id': 'rear_glass',
        'type': 'status'
    },
    'charging_port': {
        'column_id': 'microphone',
        'type': 'status'
    },
    'wireless': {
        'column_id': 'charging_port',
        'type': 'status'
    },
    'mute_vol': {
        'column_id': 'wireless',
        'type': 'status'
    },
    'power': {
        'column_id': 'mute_vol_buttons',
        'type': 'status'
    },
    'earpiece': {
        'column_id': 'power_button',
        'type': 'status'
    },
    'loudspeaker': {
        'column_id': 'earpiece_mesh',
        'type': 'status'
    },
    'wifi': {
        'column_id': 'loudspeaker',
        'type': 'status'
    },
    'bluetooth': {
        'column_id': 'wifi',
        'type': 'status'
    },
    'rear_cam': {
        'column_id': 'bluetooth',
        'type': 'status'
    },
    'rear_lens': {
        'column_id': 'rear_camera',
        'type': 'status'
    },
    'front_cam': {
        'column_id': 'rear_lens',
        'type': 'status'
    },
    'siri': {
        'column_id': 'front_camera',
        'type': 'status'
    },
    'nfc': {
        'column_id': 'siri',
        'type': 'status'
    },
    'batt_health': {
        'column_id': 'numbers',
        'type': 'number'
    },
    'haptic': {
        'column_id': 'nfc',
        'type': 'status'
    }
}

refurb_repairing = {}

refurb_selling = {}

refurb_final = {}

refurb_return = {}

refurb_backlog = {}


# Misc Dictionaries
enquiries_general = {
    'email': {
        'column_id': 'text',
        'type': 'text'
    },
    'phone': {
        'column_id': 'text0',
        'type': 'text'
    },
    'body': {
        'column_id': 'long_text',
        'type': 'text'
    },
    'fault_type': {
        'column_id': 'status6',
        'type': 'status'
    },
    'converted': {
        'column_id': 'converted',
        'type': 'status'
    },
    'zendesk_id': {
        'column_id': 'zendesk_id',
        'type': 'text'
    }
}

stuart_data = {
    'stuart_job_id': {
        'column_id': 'stuart_job_id',
        'type': 'text'
    },
    'booking_time': {
        'column_id': 'booking_time6',
        'type': 'hour'
    },
    'collection_time': {
        'column_id': 'collection_time4',
        'type': 'hour'
    },
    'delivery_time': {
        'column_id': 'delivery_time',
        'type': 'hour'
    },
    'ex_vat': {
        'column_id': 'cost__ex_vat_',
        'type': 'number'
    },
    'vat': {
        'column_id': 'vat',
        'type': 'number'
    },
    'collection_postcode': {
        'column_id': 'collection_postcode5',
        'type': 'text'
    },
    'delivery_postcode': {
        'column_id': 'delivery_postcode',
        'type': 'text'
    },
    'distance': {
        'column_id': 'distance',
        'type': 'number'
    },
    'estimated_time': {
        'column_id': 'estimated_time__mins_',
        'type': 'number'
    },
    'date': {
        'column_id': 'date',
        'type': 'date'
    },
    'collection_to_delivery': {
        'column_id': 'collection____delivery',
        'type': 'text'
    },
    'booking_to_delivery': {
        'column_id': 'booking____delivery',
        'type': 'text'
    },
    'booking_to_collection': {
        'column_id': 'booking____collection',
        'type': 'text'
    },
    'tracking_url': {
        'column_id': 'tracking_url',
        'type': 'link'
    },
    'assignment_code': {
        'column_id': 'assignment_code',
        'type': 'text'
    },
    'status': {
        'column_id': 'status',
        'type': 'status'
    }
}

wastage_item = {
    'waste_quantity': {
        'column_id': 'quantity',
        'type': 'number'
    },
    'waste_status': {
        'column_id': 'waste_status',
        'type': 'status'
    },
    'partboard_id': {
        'column_id': 'partboard_id',
        'type': 'text'
    }
}
