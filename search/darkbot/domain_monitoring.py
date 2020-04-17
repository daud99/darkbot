from django.core.mail import send_mail
from accounts.script import sendmail
from search.models import MonitorDomain, DomainEmailStatus, IndexEmail
from gatherdumps.models import Email_passwords
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from search.models import GlobalVar
breaker = False
running_state = False


def sendMail(email, subject='SOC ALERT', support_email=None, found_passwords='', found_breaches='', found_pastes='',
             found_occurrence_darkweb=''):
    subject = subject
    from_email = sendmail.EMAIL_HOST_USER
    to_list = [email, 'daudahmed870@gmail.com']
    if (support_email):
        to_list.append(support_email)
    context = {
        'email': email,
        'passwords': found_passwords,
        'breaches': found_breaches,
        'pastes': found_pastes,
        'dboccurence': found_occurrence_darkweb,
    }
    html_message = render_to_string('monitoring_domain.html', context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, to_list, html_message=html_message)
    print(f'Respective {email} is notified')


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


def get_passwords_by_email(email):
    try:
        passwords = Email_passwords.objects.filter(email__iexact=email).values_list('password', flat=True)
        password_set = set(passwords)
        unique_passwords = list(password_set)
    except Exception as e:
        print("Exception while find emails over domain")
        return None
    else:
        return unique_passwords


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


def get_darknet_occurrences(email):
    try:
        darknet_occurrences = IndexEmail.objects.filter(email__iexact=email).values_list('channel_url', flat=True)
        occurrences_list = list(darknet_occurrences)
    except Exception as e:
        print("Exception while find emails over domain")
        return None
    else:
        return occurrences_list


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


def monitor_single_email(email, domain, type):
    if type == True:
        newPasswords = get_passwords_by_email(email)
        print(newPasswords)
    else:
        newDarknetLinks = get_darknet_occurrences(email)
        print(newDarknetLinks)

    if "newPasswords" in locals():
        if newPasswords == None:
            return

    if "newDarknetLinks" in locals():
        if newDarknetLinks == None:
            return

    current_email_status = DomainEmailStatus.objects.filter(email__iexact=email, domain=domain).all()
    current_email_status = list(current_email_status)
    if (len(current_email_status)) == 0:
        oldPasswords = []
        oldDarknetLinks = []
        print(email)
        print(domain)
        new_obj = DomainEmailStatus(email=email, domain=domain)
        new_obj.save()
        print("sucessfully save")
    else:
        current_email_status = current_email_status[0]
        oldDarknetLinks = current_email_status.darknet_occurrences
        oldPasswords = current_email_status.passwords
    if ("newPasswords" in locals()):
        if (set(oldPasswords) == set(newPasswords)):
            pass
        elif (set(oldPasswords) < set(newPasswords)):
            sendMail(email, support_email=domain.support_email, found_passwords=newPasswords,
                     subject="New Password leak is found")
            # sendMail(domain.support_email, found_passwords=newPasswords, subject=str("New Password leak for "+ email+"is found"))
            print('For sure, Notify the respective user')
            DomainEmailStatus.objects.filter(email__iexact=email, domain=domain).update(passwords=newPasswords)
            print('Updated successfully DB')
        elif (set(oldPasswords) > set(newPasswords)):
            pass
        elif (set(newPasswords) - set(oldPasswords)):
            print("New set has new passwords")
            total_passwords = list(set(newPasswords) | set(oldPasswords))
            sendMail(email, support_email=domain.support_email, found_passwords=total_passwords,
                     subject="New Password leak is found")
            print('For sure, Notify the respective user')
            DomainEmailStatus.objects.filter(email__iexact=email, domain=domain).update(passwords=total_passwords)
            print('Updated successfully DB')
    if ("newDarknetLinks" in locals()):
        if (set(oldDarknetLinks) == set(newDarknetLinks)):
            pass
        elif (set(oldDarknetLinks) < set(newDarknetLinks)):
            sendMail(email, support_email=domain.support_email, found_occurrence_darkweb=newDarknetLinks,
                     subject="New DarkNet Occerrence leak is found")
            print('For sure, Notify the respective user')
            DomainEmailStatus.objects.filter(email__iexact=email, domain=domain).update(
                darknet_occurrences=newDarknetLinks)
            print('Updated successfully DB')
        elif (set(oldDarknetLinks) > set(newDarknetLinks)):
            pass
        elif (set(newDarknetLinks) - set(oldDarknetLinks)):
            total_darknet_links = list(set(oldDarknetLinks) | set(newDarknetLinks))
            sendMail(email, support_email=domain.support_email, found_occurrence_darkweb=total_darknet_links,
                     subject="New DarkNet Occerrence leak is found")
            print('For sure, Notify the respective user')
            DomainEmailStatus.objects.filter(email__iexact=email, domain=domain).update(
                darknet_occurrences=total_darknet_links)
            print('Updated successfully DB')


def monitor_emails_over_domain(domain):
    globalvars = GlobalVar.objects.filter(id=1)[0]
    breaker = globalvars.domainmonitoring
    if (breaker == True):
        return False
    else:
        emails = find_emails_over_domain(domain.domain)
        if (len(emails) == 0):
            return True
        else:
            for email in emails:
                print(email)
                monitor_single_email(email, domain, True)
        es = find_emails_over_domain_in_indexemails(domain.domain)
        if (len(es) == 0):
            return True
        else:
            for e in es:
                print(e)
                monitor_single_email(e, domain, False)
    return True


def monitor_domains():
    # global running_state, breaker
    while (True):
        globalvars = GlobalVar.objects.filter(id=1)[0]
        breaker = globalvars.domainmonitoring
        if (breaker == True):
            break
        try:
            domains = MonitorDomain.objects.all()
        except Exception as e:
            print("Exception at domaing object finding from db")
            break
        else:
            if (domains.count() == 0):
                print("No Domains found in db")
                break
            else:
                for domain in domains:
                    print(domain)
                    if (not domain.allow_monitoring):
                        print("monitoring is not allowed")
                        continue
                    else:
                        print("going to call monitor_emails_over_domain")
                        check = monitor_emails_over_domain(domain)
                        if (not check):
                            break


def stop_domain_monitoring():
    # global running_state, breaker
    # running_state = False
    # breaker = True
    GlobalVar.objects.filter(id=1).update(domainmonitoring=True)


def start_domain_monitoring():
    print("i have been called")
    # global breaker, running_state
    GlobalVar.objects.filter(id=1).update(domainmonitoring=False)
    # Do nothing if process is already running
    # breaker = False
    # running_state = True
    try:
        domains_in_queue = MonitorDomain.objects.all().count()
    except Exception as e:
        print('Something went wrong with db system')
        stop_domain_monitoring()
        return
    else:
        if domains_in_queue == 0:
            print('NO domains to monitor')
            return
        else:
            print("found a total of", domains_in_queue, " domains in queue")
            monitor_domains()
