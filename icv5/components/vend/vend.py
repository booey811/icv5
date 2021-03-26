import json
import os
import requests

import settings

vend_auth = os.environ['VENDSYS']


def get_customer(name, email, phone):

    url = "https://icorrect.vendhq.com/api/2.0/search"

    querystring = {"email": f"{email}", "type": "customers"}

    headers = {'authorization': vend_auth}

    response = requests.request("GET", url, headers=headers, params=querystring)

    formatted = json.loads(response.text)

    if formatted['data']:
        return formatted['data'][0]['id']

    else:
        return create_customer(name, email, phone)

def create_customer(name, email, phone=None):

    url = "https://icorrect.vendhq.com/api/2.0/customers"

    payload = {
        'first_name': name.split()[0],
        'last_name': name.split()[1],
        'email': email
    }

    if phone:
        payload['mobile'] = str(phone)

    payload = json.dumps(payload)

    headers = {
        'content-type': "application/json",
        'authorization': vend_auth
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    formatted = json.loads(response.text)

    return formatted['data']['id']


def create_sale(customer_id):

    payload = {
        "register_id": "02d59481-b67d-11e5-f667-b318647c76c1",
        "user_id": "0a6f6e36-8bab-11ea-f3d6-9603728ea3e6",
        "status": "SAVED",
        'customer_id': customer_id,
        "register_sale_products": [{
            "product_id": "137f1121-82a7-931b-30f6-a4a6db3fdff3",
            "quantity": 1,
            "price": 0,
            "tax": 0,
            "tax_id": "02d59481-b67d-11e5-f667-b3186463c535"
        }]
    }

    payload = json.dumps(payload)

    url = "https://icorrect.vendhq.com/api/register_sales"
    headers = {
        'content-type': "application/json",
        'authorization': vend_auth
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    formatted = json.loads(response.text)

    return formatted

def convert_to_vend(monday_object):

    try:
        name = monday_object.name
        email = monday_object.email.easy
        phone = monday_object.phone.easy
        customer_id = get_customer(name, email, phone)
        sale_object = create_sale(customer_id)
        monday_object.v_id.change_value(str(sale_object['register_sale']['id']))
        monday_object.add_to_vend.change_value('Added')

    except:
        monday_object.add_to_vend.change_value('Failed')

    finally:
        monday_object.apply_column_changes()


