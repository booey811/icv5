def added_to_enquiries_board(enquiry_body):
    result = """Thank you for your enquiry, a member of our team will be in contact as soon as possible.
    
    For convenience, your enquiry is copied below:\n\n{}\n\n{}""".format(
        enquiry_body,
        sign_off
    )
    return result


sign_off = """Kind regards,

The iCorrect Support Team

iCorrect
12 Margaret Street
London W1W 8JQ
02070998517
"""
