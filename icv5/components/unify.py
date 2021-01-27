from icv5.components.monday import boardItems_main, boardItems_reporting
from icv5.components.zendesk import ticket

main_item = boardItems_main.MainBoardItem(1002886137)
if not main_item.zendesk_id.easy:
    my_ticket = ticket.ZendeskTicket()
    my_ticket.main_id.change_value(str(main_item.id))
    user_search = ticket.ZendeskSearch().search_or_create_user(main_item)
    if user_search:
        my_ticket.ticket.requester_id = user_search.id
        new_ticket = my_ticket.client.tickets.create(my_ticket.ticket)
        main_item.zendesk_id.change_value(str(new_ticket.ticket.id))
        main_item.zendesk_url.change_value(str(new_ticket.ticket.id))
        if not main_item.phone.easy:
            main_item.phone.change_value(str(new_ticket.ticket.requester.phone))
        elif main_item.phone.easy and not new_ticket.ticket.requester.phone:
            new_ticket.ticket.requester.phone = main_item.phone.easy
            my_ticket.client.users.update(new_ticket.ticket.requester)
        main_item.zenlink.change_value('Active')
        main_item.apply_column_changes()
    else:
        print('Cannot Create User')