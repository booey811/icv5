from pprint import pprint as p
import time

from moncli.entities import create_column_value
from moncli import ColumnType

from icv5.components.monday.boardItems_misc import StuartDataItem
from icv5.components.monday import boardItems_main, boardItems_inventory, manage, boardItems_reporting
from icv5.components.stuart import stuart

main = boardItems_main.MainBoardItem(1002886137)

test = boardItems_reporting.FinancialItem(1046233015)

test.process_repair_data()