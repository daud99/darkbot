from gatherdumps.scripts.dumpsCollectors.brocard_dumps import BrocardCrawler
from gatherdumps.scripts.dumpsCollectors.brocard_cvv import Brocard_CvvFinder
from gatherdumps.scripts.dumpsCollectors.meccadumps_cvv import Meccadumps_CvvFinder
from gatherdumps.scripts.dumpsCollectors.meccadumps_dump import Meccadumps_DumpFinder
from search.api import misc
import time
from gatherdumps.models import Country, CardDump, CardCvv, Email_passwords, CardMarket, Checkpoint, CrawlerAccess
from search.darkbot.crawl import emails_with_channel
from gatherdumps.scripts.common.check_crawler_access import update_cancel_permission, update_start_permission
from gatherdumps.scripts.db.checkpointing import get_checkpoint, update_checkpoint, get_index_checkpoint
from gatherdumps.scripts.common.email_validation import validateEmail
from gatherdumps.scripts.db.get_file_paths import get_email_file_path, update_file_path
from gatherdumps.scripts.common.check_crawler_access import check_breaker_state, update_breaker_state


def collect_BrocardDumps(identity):
    update_start_permission(100, False)
    update_breaker_state(100, False)
    countries = Country.objects.all()
    checkpoint = get_checkpoint(identity)
    current_market = CardMarket.objects.get(market_identity__exact=2)
    market_name = current_market.name
    m_url = current_market.url
    m_url_base = m_url.split('.')[0]
    if ('://' in m_url_base):
        m_url_base = m_url_base.split('://')[1]
    m_username = current_market.username
    m_password = current_market.password
    driver = BrocardCrawler(m_url, m_username, m_password)
    driver.create_driver()
    driver.login()
    driver.visit_dumps()
    '''
    current_index = checkpoint.checkpoint_index
    '''
    # counter = 0
    start_index = checkpoint.next_index
    for i in range(start_index, len(countries)):
        if (check_breaker_state(100)):
            break
        # i = i+1
        j = i + 1
        print('next country will be at index', j)
        done_scraping = False

        try:
            current_country = countries[i].name
            current_country = current_country.strip()
            # country_alpha3 = name_to_alpha3(current_country)
            country_alpha3 = countries[i].alpha3_code
            print(country_alpha3)
            if country_alpha3 == None:
                continue

            CardDump.objects.filter(source__icontains=m_url_base, country__iexact=country_alpha3).delete()
            done_scraping = driver.perform_crScrap_process(current_country, countries[i].id)
        except Exception as e:
            print(e)
            # continue

        else:
            if (done_scraping == True):
                k = i + 1
                if (k >= countries.count()):
                    k = 0
                update_checkpoint(checkpoint, k)
            else:
                print('No update in checkpoint')

    driver.close_driver()
    driver = None
    # update_start_permission(100, True)
    return "Done BroCard Dumps"


def collect_BrocardCvvs(identity):
    update_breaker_state(100, False)
    countries = Country.objects.all()
    update_start_permission(100, False)
    checkpoint = get_checkpoint(identity)
    current_market = CardMarket.objects.get(market_identity__exact=2)
    market_name = current_market.name
    m_url = current_market.url
    m_url_base = m_url.split('.')[0]
    if ('://' in m_url_base):
        m_url_base = m_url_base.split('://')[1]
    m_username = current_market.username
    m_password = current_market.password
    driver = Brocard_CvvFinder(m_url, m_username, m_password)
    driver.create_driver()
    driver.login()
    driver.visit_cvvs()
    # counter = 0
    start_index = checkpoint.next_index
    for i in range(start_index, len(countries)):
        if (check_breaker_state(100)):
            break
        # i = i+1
        j = i + 1
        print('next country will be at index', j)
        done_scraping = False
        try:
            current_country = countries[i].name
            current_country = current_country.strip()
            # country_alpha3 = name_to_alpha3(current_country)
            country_alpha3 = countries[i].alpha3_code
            print(country_alpha3)
            if country_alpha3 == None:
                continue

            CardCvv.objects.filter(source__icontains=m_url_base, country__iexact=country_alpha3).delete()
            # print(CardDump.objects.all().count())
            done_scraping = driver.perform_crScrap_process(current_country, countries[i].id)
        except Exception as e:
            print(e)
            # continue
        else:
            if (done_scraping == True):
                k = i + 1
                if (k >= countries.count()):
                    k = 0
                update_checkpoint(checkpoint, k)
            else:
                print('No update in checkpoint')
    driver.close_driver()
    driver = None
    return "Done BroCard Dumps"


def collect_MeccaDumps(identity):
    update_breaker_state(100, False)
    countries = Country.objects.all()
    update_start_permission(100, False)
    checkpoint = get_checkpoint(identity)
    current_market = CardMarket.objects.get(market_identity__exact=1)
    market_name = current_market.name
    m_url = current_market.url
    m_url_base = m_url.split('.')[0]
    if ('://' in m_url_base):
        m_url_base = m_url_base.split('://')[1]
    m_username = current_market.username
    m_password = current_market.password
    driver = Meccadumps_DumpFinder(m_url, m_username, m_password)
    driver.create_driver()

    driver.login()
    driver.visit_cvvs()

    # counter = 0
    start_index = checkpoint.next_index
    for i in range(start_index, len(countries)):
        if (check_breaker_state(100)):
            break
        # i = i+1
        j = i + 1
        print('next country will be at index', j)
        done_scraping = False
        try:
            current_country = countries[i].name
            current_country = current_country.strip()
            # country_alpha3 = name_to_alpha3(current_country)
            country_alpha3 = countries[i].alpha3_code
            print(country_alpha3)
            if country_alpha3 == None:
                continue

            CardDump.objects.filter(source__icontains=m_url_base, country__iexact=country_alpha3).delete()

            done_scraping = driver.perform_crScrap_process(current_country, countries[i].id)
        except Exception as e:
            print(e)
            # continue
        else:
            if (done_scraping == True):
                k = i + 1
                if (k >= countries.count()):
                    k = 0
                update_checkpoint(checkpoint, k)
            else:
                print('No update in checkpoint')
    driver.close_driver()
    driver = None
    return "Done MD"


def collect_MeccaCvvs(identity):
    countries = Country.objects.all()
    update_breaker_state(100, False)
    update_start_permission(100, False)
    checkpoint = get_checkpoint(identity)
    current_market = CardMarket.objects.get(market_identity__exact=1)
    market_name = current_market.name
    m_url = current_market.url
    m_url_base = m_url.split('.')[0]
    if ('://' in m_url_base):
        m_url_base = m_url_base.split('://')[1]
    m_username = current_market.username
    m_password = current_market.password
    driver = Meccadumps_CvvFinder(m_url, m_username, m_password)

    driver.create_driver()

    driver.login()
    driver.visit_cvvs()

    # counter = 0
    start_index = checkpoint.next_index
    for i in range(start_index, len(countries)):
        if (check_breaker_state(100)):
            break
        # i = i+1
        j = i + 1
        print('next country will be at index', j)
        done_scraping = False
        try:

            current_country = countries[i].name
            current_country = current_country.strip()
            # country_alpha3 = name_to_alpha3(current_country)
            country_alpha3 = countries[i].alpha3_code
            print(country_alpha3)
            if country_alpha3 == None:
                continue

            CardCvv.objects.filter(source__icontains=m_url_base, country__iexact=country_alpha3).delete()
            done_scraping = driver.perform_crScrap_process(current_country, countries[i].id)
        except Exception as e:
            print(e)
            # continue
        else:
            if (done_scraping == True):
                k = i + 1
                if (k >= countries.count()):
                    k = 0
                update_checkpoint(checkpoint, k)
            else:
                print('No update in checkpoint')
    driver.close_driver()
    driver = None
    return "Done MD"
    # data.close()


def collect_emails_over_forums(indentity):
    update_start_permission(200, False)
    emails_with_channel()
    return "DDD"


def daud_collect_email_passwords(identity):
    print('yes')
    update_start_permission(identity, False)
    print('no')
    update_file_path(identity, "In Progress")
    print('verry no')
    try:
        file = get_email_file_path(identity)
        print(file)
        if file == None:
            print('no file path found of identifier 300')
            update_file_path(identity, "failed")
            return
    except Exception as e:
        update_file_path(identity, "failed")
        print(
            'something is wrong while fetching the data form the File path table please examine the fill data and make sure identifier is 300')
        return
    else:
        source = file[0]
        path = file[1]
        breakpoint = file[2]
        try:
            f = open(path)
        except Exception as e:
            print("error opening file")
            update_file_path(identity, "failed")
            return
        else:
            f.seek(0)
            while (True):
                try:
                    currentLine = f.readline()
                except Exception as e:
                    print('exception while reading the line so moving to next line')
                    continue
                if currentLine == "":
                    print("current line is the empty string so file is finished")
                    break
                elif currentLine == None:
                    print("current line is None")
                    break
                else:
                    currentLine = (currentLine.encode('ascii', 'ignore')).decode('utf-8').strip()
                    currentLine = currentLine.rstrip(r'\n')
                    currentLine = currentLine.split(breakpoint)
                    # print(currentLine)
                    if len(currentLine) == 2:
                        email = currentLine[0]
                        password = currentLine[1]
                    else:
                        continue
                    email = email.strip()
                    password = password.strip()
                    email = email.strip(' \"{}[]()#$!')
                    email = email.strip("'")
                    password = password.strip("'")
                    password = password.strip('"')
                    try:
                        if identity == 300:
                            email = validateEmail(email)
                            if (email):
                                email = email.lower()
                            else:
                                continue
                            before_at, domain = misc.returnTwo(email)
                            currentEmail = Email_passwords(email=email, password=password, source=source, domain=domain,
                                                           before_at=before_at)
                            currentEmail.save()
                        elif identity == 302:
                            if (email):
                                email = email.lower()
                            else:
                                continue
                            currentEmail = Email_passwords(username=email, password=password, source=source)
                            currentEmail.save()
                    except Exception as e:
                        print("error saving username may be repetition")
                        continue

                # if s == 34:
                #     break
        f.close()
        update_file_path(identity, "complete")
        update_start_permission(identity, True)
        print('every thing is fine')


def collect_email_passwords(identity):
    update_start_permission(300, False)
    update_breaker_state(300, False)
    # global email_pass_seek_point, data
    email_pass_seek_point = 0
    # BASE= os.path.dirname(os.path.abspath(__file__))
    # data = open(os.path.join(BASE, "files/outlook.txt"), 'r')
    try:
        path = get_email_file_path(300)
        data = open(path[0], 'r')
    except Exception as e:
        messages.warning(request, 'Something is wrong with file path')
        return render(request, link)
    else:
        if (path == None):
            messages.warning(request, 'Something is wrong with file path')
            return render(request, link)
    checkpoint = get_index_checkpoint(1002)
    try:
        time.sleep(10)
        seek_point = checkpoint.next_index
        print(seek_point)
        data.seek(seek_point)
        print('Seeked')
    except Exception as e:
        print('Could not move to line')
    # Email_passwords.objects.all().delete()
    em_pass = None
    try:
        em_pass = data.readline()
        seek_point = seek_point + 1
    except Exception as e:
        em_pass = None
    start_time = time.time()

    while (True):
        if (check_breaker_state(300)):
            break
        try:
            if not em_pass:
                break
            # email_pass_seek_point = email_pass_seek_point + 1
            em_pass = (em_pass.encode('ascii', 'ignore')).decode('utf-8').strip()
            break_point = path[1]
            em_pass = em_pass.split(break_point)
            email = em_pass[0]
            passw = em_pass[1]
            email = email.strip()
            passw = passw.strip()
            email = email.strip(' \"{}[]()#$!')
            email = email.strip("'")
            passw = passw.strip("'")
            passw = passw.strip('"')

            try:
                email = validateEmail(email)
                if (email):
                    email = email.lower()
                    obj = Email_passwords(email=email, password=passw)
                    obj.save()
                    print("Saved to db")
            except Exception as e:
                print("No need to save it")
            em_pass = data.readline()
            seek_point = seek_point + 1
        except Exception as e:
            print('Exp Goto next line')
            try:
                em_pass = data.readline()
            except AttributeError as e:
                break
            except Exception as e:
                break
            else:

                continue
    try:

        if (seek_point > 0):
            update_checkpoint(checkpoint, seek_point)
    except Exception as e:
        print(e)
    data = None
    return "MM"