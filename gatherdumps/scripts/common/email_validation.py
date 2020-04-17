from email_validator import validate_email, EmailNotValidError

def validateEmail(email):
    try:
        v = validate_email(email) # validate and get info
        email = v["email"] # replace with normalized form
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        print(str(e))
        return None
    else:
        return email

if __name__ == "__main__":
    mail = validateEmail('tesT@Tranchulas.com')
    print(mail)