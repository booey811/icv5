import json
import time

import flask

from icv5.components import unify, stuart
from icv5.components.monday import boardItems_main, boardItems_refurbs, boardItems_inventory, manage, boardItems_misc, \
    boardItems_reporting, boardItems_financial
from icv5.components.phonecheck import phonecheck
from icv5.components.zendesk import ticket
from icv5.components.stuart import stuart

# APP SET UP
app = flask.Flask(__name__)


# APP FUNCTIONS
def monday_handshake(webhook):
    """Takes webhook information, authenticates if required, and decodes information

    Args:
        webhook (request): Payload received from Monday's Webhooks

    Returns:
        dictionary: contains various information from Monday, dependent on type of webhook sent
    """
    data = webhook.decode('utf-8')
    data = json.loads(data)
    if "challenge" in data.keys():
        authtoken = {"challenge": data["challenge"]}
        return [False, authtoken]
    else:
        return [True, data]


# ROUTES // ++++++++++++ TEST ROUTE ++++++++++++ \\
@app.route("/811/test", methods=["POST"])
def test_route():
    start_time = time.time()
    info = flask.request.get_data()
    print(info)
    print("--- %s seconds ---" % (time.time() - start_time))
    return "TEST COMPLETE"


# ROUTES // ++++++++++++ TEST ROUTE == MONDAY ++++++++++++ \\
@app.route("/811/test/monday", methods=["POST"])
def test_route_monday():
    start_time = time.time()
    print("Zenlink Column Adjustment")
    webhook = flask.request.get_data()
    # Authenticate & Create Object
    data = monday_handshake(webhook)
    if data[0] is False:
        return data[1]
    else:
        data = data[1]
    print(data)
    print("--- %s seconds ---" % (time.time() - start_time))
    return "MONDAY TEST COMPLETE"


# MONDAY ROUTES == Main Board
# Zenlink -> Create Connection
@app.route('/monday/main/zenlink/create', methods=['POST'])
def zenlink_creation():
    """Creates a ticket on Zendesk and links them'"""

    start_time = time.time()
    webhook = flask.request.get_data()
    # Authenticate & Create Object
    data = monday_handshake(webhook)
    if data[0] is False:
        return data[1]
    else:
        data = data[1]

    main_item = boardItems_main.MainBoardItem(item_id=data['event']['pulseId'], webhook_payload=data)
    if not main_item.zendesk_id.easy:
        my_ticket = ticket.ZendeskTicket()
        my_ticket.adjust_custom_field('main_id', main_item.id)
        user_search = ticket.ZendeskSearch().search_or_create_user(main_item)
        if user_search:
            my_ticket.ticket.requester_id = user_search.id
            new_ticket = my_ticket.client.tickets.create(my_ticket.ticket)
            main_item.zendesk_id.change_value(str(new_ticket.ticket.id))
            main_item.zendesk_url.change_value(
                [
                    str(new_ticket.ticket.id),
                    str('https://icorrect.zendesk.com/agent/tickets/{}'.format(new_ticket.ticket.id))
                ]
            )
            if not main_item.phone.easy:
                main_item.phone.change_value(str(new_ticket.ticket.requester.phone))
            elif main_item.phone.easy and not new_ticket.ticket.requester.phone:
                new_ticket.ticket.requester.phone = main_item.phone.easy
                my_ticket.client.users.update(new_ticket.ticket.requester)
            main_item.zenlink.change_value('Active')
            main_item.apply_column_changes()
        else:
            print('Cannot Create User')

    print("--- %s seconds ---" % (time.time() - start_time))
    return 'Main Board Zendesk Link Creation Complete'


# MONDAY ROUTES == Book Collection
# be_courier_collection ==> Attempting Booking
@app.route('/monday/couriers/collect', methods=["POST"])
def book_courier_collection():
    """This route is for booking a stuart courier collection'"""

    start_time = time.time()
    webhook = flask.request.get_data()
    # Authenticate & Create Object
    data = monday_handshake(webhook)
    if data[0] is False:
        return data[1]
    else:
        data = data[1]

    main_item = boardItems_main.MainBoardItem(item_id=data["event"]["pulseId"], webhook_payload=data)
    courier = stuart.StuartClient(main_item=main_item)

    try:
        job_payload = courier.validate_job_details('collection')
        courier.book_courier_job(job_payload)
    except (stuart.DistanceTooGreat or stuart.EmailInvalid or stuart.CannotGeocodeAddress or
            stuart.UnknownValidationError or stuart.CourierDetailsMissing or stuart.PhoneNumberInvalid):
        pass

    print("--- %s seconds ---" % (time.time() - start_time))
    return 'Courier Collection Booking Route Complete'


# MONDAY ROUTES == Book Return
# be_courier_return ==> Attempting Booking
@app.route('/monday/couriers/deliver', methods=["POST"])
def book_courier_return():
    """This route is for booking a stuart courier collection'"""

    start_time = time.time()
    webhook = flask.request.get_data()
    # Authenticate & Create Object
    data = monday_handshake(webhook)
    if data[0] is False:
        return data[1]
    else:
        data = data[1]

    main_item = boardItems_main.MainBoardItem(item_id=data["event"]["pulseId"], webhook_payload=data)
    courier = stuart.StuartClient(main_item=main_item)

    try:
        job_payload = courier.validate_job_details('delivery')
        courier.book_courier_job(job_payload)
    except (stuart.DistanceTooGreat or stuart.EmailInvalid or stuart.CannotGeocodeAddress or
            stuart.UnknownValidationError or stuart.CourierDetailsMissing or stuart.PhoneNumberInvalid):
        pass

    print("--- %s seconds ---" % (time.time() - start_time))
    return 'Courier Delivery Booking Route Complete'


# MONDAY ROUTES == Inventory Movements Board
@app.route('/monday/inventory/reporting/stock', methods=["POST"])
def add_products_to_repair():
    """This Route will add to the inventory movements board"""

    start_time = time.time()
    webhook = flask.request.get_data()
    # Authenticate & Create Object
    data = monday_handshake(webhook)
    if data[0] is False:
        return data[1]
    else:
        data = data[1]

    reporting = boardItems_reporting.InventoryMovementItem(data["event"]["pulseId"])
    reporting.remove_stock()

    print("--- %s seconds ---" % (time.time() - start_time))
    return 'Inventory Reporting Route Complete'


# MONDAY ROUTES == Stock Counts Board
# Count Status -> Complete
@app.route('/monday/inventory/stock-count', methods=["POST"])
def add_stock_count_to_inventory():
    """This Route will add to the inventory levels when a stock count is complete"""

    start_time = time.time()
    webhook = flask.request.get_data()
    # Authenticate & Create Object
    data = monday_handshake(webhook)
    if data[0] is False:
        return data[1]
    else:
        data = data[1]

    count_item = boardItems_inventory.InventoryStockCountItem(item_id=data["event"]["pulseId"], webhook_payload=data)

    count_item.process_stock_count()

    print("--- %s seconds ---" % (time.time() - start_time))
    return 'Stock Count Item Route Complete'


# MONDAY ROUTES == Stock Orders Board
# BUTTON: Add to Stock
@app.route('/monday/inventory/order/received', methods=["POST"])
def add_order_to_stock():
    """This route adds to the necessary stock levels and adjusts the supply price accordingly"""

    start_time = time.time()
    webhook = flask.request.get_data()
    # Authenticate & Create Object
    data = monday_handshake(webhook)
    if data[0] is False:
        return data[1]
    else:
        data = data[1]

    order_item = boardItems_inventory.InventoryOrderItem(item_id=data["event"]["pulseId"])

    order_item.add_received_items_to_stock()

    print("--- %s seconds ---" % (time.time() - start_time))
    return 'Stock Order Received Route Complete'


# MONDAY ROUTES == Financial Board
# Repair Profile ==> Do Now!
@app.route('/monday/reporting/financial/get-parts', methods=["POST"])
def generate_repair_subitems():
    """This Route processes financial board creations'"""

    start_time = time.time()
    webhook = flask.request.get_data()
    # Authenticate & Create Object
    data = monday_handshake(webhook)
    if data[0] is False:
        return data[1]
    else:
        data = data[1]

    finance = boardItems_financial.FinancialBoardItem(item_id=data["event"]["pulseId"], webhook_payload=data)
    finance.construct_repairs_profile()

    print("--- %s seconds ---" % (time.time() - start_time))
    return 'Financial Reporting Repairs Profile Route Complete'


# MONDAY ROUTES == Financial Board
# Stock Adjustment ==> Do Now!
@app.route('/monday/reporting/financial/eod', methods=["POST"])
def process_repair_subitems():
    """This Route processes financial board creations'"""

    start_time = time.time()
    webhook = flask.request.get_data()
    # Authenticate & Create Object
    data = monday_handshake(webhook)
    if data[0] is False:
        return data[1]
    else:
        data = data[1]

    finance = boardItems_financial.FinancialBoardItem(item_id=data["event"]["pulseId"], webhook_payload=data)
    finance.stock_deductions_and_recording()

    print("--- %s seconds ---" % (time.time() - start_time))
    return 'Financial Reporting Repairs Profile Route Complete'

# MONDAY ROUTES == Financial Board
# Parts Status ==> Void
@app.route('/monday/reporting/financial/void', methods=["POST"])
def void_financial_entry():
    """This Route processes financial board creations'"""

    start_time = time.time()
    webhook = flask.request.get_data()
    # Authenticate & Create Object
    data = monday_handshake(webhook)
    if data[0] is False:
        return data[1]
    else:
        data = data[1]

    finance = boardItems_financial.FinancialBoardItem(item_id=data["event"]["pulseId"], webhook_payload=data)
    finance.disassemble_repairs_profile()

    print("--- %s seconds ---" % (time.time() - start_time))
    return 'Financial Void Route Complete'


# MONDAY ROUTES == Enquiries Board
# ** -> Item Creation
@app.route('/monday/enquiry/received', methods=["POST"])
def create_zendesk_ticket_for_enquiry():
    """This route is for getting data from Phonecheck's database (grabbed with info from the 'Received' board),
    and creating a pulse with corresponding statuses on 'Repairing'"""

    start_time = time.time()
    webhook = flask.request.get_data()
    # Authenticate & Create Object
    data = monday_handshake(webhook)
    if data[0] is False:
        return data[1]
    else:
        data = data[1]

    monday_enquiry = boardItems_misc.GeneralEnquiryItem(data["event"]["pulseId"])
    searcher = ticket.ZendeskSearch()
    new_zenpy_ticket = searcher.create_ticket(monday_enquiry, 'enquiries')
    ticket_audit = searcher.client.tickets.create(new_zenpy_ticket)
    monday_enquiry.zendesk_id.change_value(str(ticket_audit.ticket.id))
    monday_enquiry.apply_column_changes(verbose=True)

    print("--- %s seconds ---" % (time.time() - start_time))
    return 'Zendesk Query Creation Complete'


# ROUTES // ++++++++++++ ZENDESK ++++++++++++ \\
# ZENDESK ROUTES == Enquiries Board Updates
# Add to Monday:Checked and BoardID Present
@app.route('/zendesk/update_enquiries', methods=["POST"])
def update_enquiry_board_with_destination():
    """This route is for getting data from Phonecheck's database (grabbed with info from the 'Received' board),
    and creating a pulse with corresponding statuses on 'Repairing'"""

    start_time = time.time()
    webhook = flask.request.get_data().decode()
    data = json.loads(webhook)

    enquiry = boardItems_misc.GeneralEnquiryItem(data['enquiry_id'])
    enquiry.converted.change_value('Added to Main Board')
    enquiry.apply_column_changes()

    print("--- %s seconds ---" % (time.time() - start_time))
    return 'Zendesk Query Creation Complete'


# ROUTES // STUART
# Callback Function
@app.route("/stuart/updates", methods=["POST"])
def stuart_responses():

    data = flask.request.get_data().decode("utf-8")

    data = json.loads(data)

    if data['event'] == 'job' and data['type'] == 'update':

        job_id = data["data"]["id"]
        data_item = boardItems_misc.StuartDataItem.get_data_item(job_id)

        if data['data']['currentDelivery']["status"] == 'delivering':
            print('COLLECTION UPDATE')
            data_item.update_timing('collecting')
            print("Has Been Picked Up")

        elif data['data']['currentDelivery']["status"] == 'delivered':
            print('DELIVERING UPDATE')
            data_item.update_timing('delivering')
            print("Has Been Delivered")

    return "Stuart Webhook Route Complete"


if __name__ == "__main__":
    app.run(load_dotenv=True)
