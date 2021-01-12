import json
import time

import flask

from icv5.components import unify
from icv5.components.monday import boardItems_main, boardItems_refurbs, boardItems_inventory, manage

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
@app.route('/monday/refurb-phones/phonecheck', methods=["POST"])
def get_phonecheck_details_and_transfer():
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

    refurb = unify.UnifiedObject(data)
    refurb.received = refurb.create_monday_object(data['event']['pulseId'], 'refurb_received')

    for item in vars(refurb.received):
        print(item.index)

    print("--- %s seconds ---" % (time.time() - start_time))

    return 'Refurb Get Phonecheck Data Route Complete'


if __name__ == "__main__":
    app.run(load_dotenv=True)
