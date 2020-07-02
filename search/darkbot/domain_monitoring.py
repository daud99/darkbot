from search.models import IndexEmail
from gatherdumps.models import Email_passwords

def find_emails_over_domain(domain_name):
    try:
        domain_name_in_email = '@' + domain_name
        emails = Email_passwords.objects.filter(email__icontains=domain_name_in_email).values_list('email', flat=True)
        emails_set = set(emails)
        emails_from_index_forums = IndexEmail.objects.filter(email__icontains=domain_name_in_email).values_list('email',
                                                                                                                flat=True)
        index_email_set = set(emails_from_index_forums)
        total_emails_set = emails_set | index_email_set
        unique_emails = list(total_emails_set)
    except Exception as e:
        print(e)
        print("Exception while find emails over domain")
        return []
    else:
        return unique_emails


def find_emails_over_domain_in_indexemails(domain_name):
    try:
        domain_name_in_email = '@' + domain_name
        emails = IndexEmail.objects.filter(email__icontains=domain_name_in_email).values_list('email', flat=True)
        for each in emails:
            print(each)
        emails_set = set(emails)
        unique_emails = list(emails_set)
    except Exception as e:
        print("Exception while find emails over domain")
        return []
    else:
        return unique_emails


def get_passwords_by_email_for_report(email):
    try:
        passwords = Email_passwords.objects.filter(email__iexact=email).values()
        for each in passwords:
            print(each)
        # password_set = set(passwords)
        unique_passwords = list(passwords)
    except Exception as e:
        print("Exception while find emails over domain")
        return None
    else:
        return unique_passwords


def get_darknet_occurrences_for_report(email):
    try:
        darknet_occurrences = IndexEmail.objects.filter(email__iexact=email).values()
        print(darknet_occurrences)
        occurrences_list = list(darknet_occurrences)
    except Exception as e:
        print("Exception while find emails over domain")
        return None
    else:
        return occurrences_list

