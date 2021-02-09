from pprint import pprint as p

from icv5.components.monday.boardItems_misc import StuartDataItem
from icv5.components.monday import boardItems_main
from icv5.components.stuart import stuart


# main_item = boardItems_main.MainBoardItem(item_id=1002886137, webhook_payload={
#     'event': {
#         'userId': 4251271
#     }
# })
#
# courier = stuart.StuartClient(main_item=main_item)
#
# try:
#     job_payload = courier.validate_job_details('collection')
#     courier.book_courier_job(job_payload)
# except (stuart.DistanceTooGreat or stuart.EmailInvalid or stuart.CannotGeocodeAddress or
#         stuart.UnknownValidationError or stuart.CourierDetailsMissing or stuart.PhoneNumberInvalid):
#     pass
#
