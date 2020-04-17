from gatherdumps.models import CardCvv, CardDump, Email_passwords
from gatherdumps.scripts.common.email_validation import validateEmail
def move_email_pass_to_db(email, passw):
    #print('hhh')
    try:
        email = validateEmail(email)
        if (not email):
            print('Not a valid email')
            return False
        obj = Email_passwords(email=email, password=passw)
        obj.save()
        print('Saved to db')
    except Exception as e:
        print('Email will not be moved from ghostfr to db')
        print(e)
def push_mails_to_db(email_passw):
    for x in email_passw:
        move_email_pass_to_db(x[0],x[1])
 