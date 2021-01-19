import json
import time

import flask

from icv5.components import unify
from icv5.components.monday import boardItems_main, boardItems_refurbs, boardItems_inventory, manage, boardItems_misc
from icv5.components.phonecheck import phonecheck
from icv5.components.zendesk import ticket

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


# ROUTES // ++++++++++++ MONDAY ++++++++++++ \\
# MONDAY ROUTES == Refurbishment Boards
# Refurbs [Received -> Tested]
# @app.route('/monday/refurb-phones/phonecheck', methods=["POST"])
# def get_phonecheck_details_and_transfer():
#     """This route is for getting data from Phonecheck's database (grabbed with info from the 'Received' board),
#     and creating a pulse with corresponding statuses on 'Repairing'"""
#
#     start_time = time.time()
#     webhook = flask.request.get_data()
#     # Authenticate & Create Object
#     data = monday_handshake(webhook)
#     if data[0] is False:
#         return data[1]
#     else:
#         data = data[1]
#
#     refurb = unify.UnifiedObject(data)
#     refurb.received = refurb.create_monday_object(data['event']['pulseId'], 'refurb_received')
#     checks = phonecheck.PhoneCheckResult(refurb.received.imei)
#     refurb.received.process_phonecheck_results(checks)
#
#     print("--- %s seconds ---" % (time.time() - start_time))
#
#     return 'Refurb Get Phonecheck Data Route Complete'
#


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
    ticket.ZendeskSearch().create_ticket_enquiry(monday_enquiry, monday_enquiry.body.easy)
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


if __name__ == "__main__":
    app.run(load_dotenv=True)


