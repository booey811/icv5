from pprint import pprint as p
import time
import os
import requests
import json

from moncli.entities import create_column_value
from moncli import ColumnType
import settings
from zenpy.lib.api_objects import CustomField
from tests import conftest

from icv5.components.monday.boardItems_misc import StuartDataItem

from icv5.components.monday import boardItems_main, boardItems_inventory, boardItems_reporting, manage, boardItems_financial, boardItems_misc
from icv5.components.stuart import stuart
from icv5.components.zendesk import ticket
from icv5.components.zendesk.assets import custom_fields

from pprint import pprint as p

# ============================================================ TEST VARIABLES ============================================================
gabe_id = 4251271
data = {'event': {'userId': '4251271'}}






# ============================================================ TEST VARIABLES ============================================================
