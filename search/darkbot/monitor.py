from search.models import IndexEmail
from search.darkbot.pwnedorNot_new import HaveIBeenPwned



def checkEmailBreaches(email):
    driver = HaveIBeenPwned()
    try:
        driver.search_by_email(email)
        breaches = driver.retrieve_breaches()
    except Exception as e:
        driver.close_driver()
    else:
        driver.close_driver()
        breaches = breaches["breaches"]
        for each in breaches:
            if each["company"][-1] == ":":
                each["company"] = each["company"][:-1]
        print("breaches method")
        # print(breaches)
        return breaches


def pasteSearch(email):
    driver = HaveIBeenPwned()
    try:
        driver.search_by_email(email)
        pastes = driver.retrieve_pastes()
    except Exception as e:
        driver.close_driver()
    else:
        driver.close_driver()
        return pastes

def getEmailPresenceOnDarkweb(email):
    mylist = IndexEmail.objects.filter(email__iexact=email).values()
    mylist = list(mylist)
    return mylist





