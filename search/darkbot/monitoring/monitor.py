from search.models import GlobalVar, MonitorAsset, CurrentAssetStatus
from search.api import views
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from accounts.script import sendmail

class Monitor():

    def __init__(self, type, leakCheck=False):
        self.__type = type

    def startMonitoring(self):
        GlobalVar.objects.filter(type=self.__type).update(monitoring=True)
        assets = MonitorAsset.objects.filter(asset_type=self.__type).count()
        if assets == 0:
            self.stopMonitoring()
        else:
            assets = MonitorAsset.objects.filter(asset_type=self.__type)
            obj = {"type": self.__type, "wildcard": 'false', "regex": 'false'}
            while True:
                breaker = GlobalVar.objects.get(type=self.__type)
                if not breaker.monitoring:
                    break
                for each in assets:
                    breaker = GlobalVar.objects.get(type=self.__type)
                    if not breaker.monitoring:
                        break
                    if not (each.allow_monitoring):
                        continue
                    obj["query"] = each.asset
                    raw_record_db = views.getRecordsFromDB(obj)
                    record_db = views.parseDbResponse(raw_record_db)
                    if each.allow_external == True:
                        raw_record_leakcheck = views.leakCheck(obj)
                        record_leakcheck = views.parseLeakCheckResponse(raw_record_leakcheck)
                        object = {"res1": record_db, "res2": record_leakcheck}
                        current_records = views.mergeResponse(object)

                    else:
                        current_records = list(record_db)

                    try:
                        save_records = CurrentAssetStatus.objects.get(asset__asset=each.asset)
                        save_records = list(save_records.records)
                        diff = Monitor.compareLists(current_records, save_records)
                        if len(save_records) != 0:
                            if (len(current_records) == len(save_records) and diff) or (len(current_records) < len(save_records) and diff):
                                pass
                            else:
                                CurrentAssetStatus.objects.filter(asset__asset=each.asset).update(records=current_records)
                                Monitor.sendMail(each.support_email, "SOC ALERT", diff)


                    except Exception as e:
                        continue


    def stopMonitoring(self):
        GlobalVar.objects.filter(type=self.__type).update(monitoring=False)


    @staticmethod
    def compareLists(list1, list2):
        array = []
        for i in list1:
            if i not in list2:
                array.append(i)

        if array == []:
            return True

        return array

    @staticmethod
    def sendMail(email, subject='SOC ALERT', found_passwords='', found_breaches='', found_pastes='',
                 found_occurrence_darkweb=''):
        subject = subject
        from_email = sendmail.EMAIL_HOST_USER
        to_list = ['daudahmed870@gmail.com']
        context = {
            'email': email,
            'passwords': found_passwords,
            'breaches': found_breaches,
            'pastes': found_pastes,
            'dboccurence': found_occurrence_darkweb,
        }
        html_message = render_to_string('monitoring_email.html', context)
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, from_email, to_list, html_message=html_message)
        print(f'Respective {email} is notified')