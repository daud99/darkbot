from search.models import GlobalVar, MonitorAsset, CurrentAssetStatus
from search.api import views
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from accounts.script import sendmail
import logging

logger = logging.getLogger(__name__)

class Monitor():
    '''
    Monitor class contains the logic for monitoring an asset of given type
    :param type: The type of the asset
    :type type: str
    '''


    def __init__(self, type, leakCheck=False):
        self.__type = type

    def startMonitoring(self):
        '''
        startMonitoring method keeps on checking for the new records until the monitoring option for the given asset type isn't set to False in DB
        '''

        GlobalVar.objects.filter(type=self.__type).update(monitoring=True)
        assets = MonitorAsset.objects.filter(asset_type=self.__type).count()
        if assets == 0:
            logger.info("The monitoring is not getting started because no asset is found")
            self.stopMonitoring()
        else:
            assets = MonitorAsset.objects.filter(asset_type=self.__type)
            obj = {"type": self.__type, "wildcard": 'false', "regex": 'false'}
            while True:
                breaker = GlobalVar.objects.get(type=self.__type)
                if not breaker.monitoring:
                    logger.info("Monitoirng is getting turned off")
                    break
                for each in assets:
                    breaker = GlobalVar.objects.get(type=self.__type)
                    if not breaker.monitoring:
                        break
                    if not (each.allow_monitoring):
                        logger.info("Monitoring is not allowed for asset = "+each.asset)
                        continue
                    obj["query"] = each.asset
                    raw_record_db = views.getRecordsFromDB(obj)
                    record_db = views.parseDbResponse(raw_record_db)
                    if each.allow_external == True:
                        logger.info("Getting data from external API is enable for asset = "+each.asset)
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
                        # if len(save_records) != 0:
                        if (len(current_records) == len(save_records) and diff) or (len(current_records) < len(save_records) and diff):
                            logger.info("no new record find for "+each.asset)
                            pass
                        else:
                            logger.info("new record find for "+each.asset)
                            CurrentAssetStatus.objects.filter(asset__asset=each.asset).update(records=current_records)
                            Monitor.sendMail(each.support_email, "SOC ALERT", diff)


                    except Exception as e:
                        logger.exception(e)
                        continue


    def stopMonitoring(self):
        '''
        stopMonitoring function sets the monitoring for a given asset type in GlobalVar to False indicating monitoring is not active
        '''

        GlobalVar.objects.filter(type=self.__type).update(monitoring=False)


    @staticmethod
    def compareLists(list1, list2):
        '''
        The method use for checking that to list of dictionaries are same or not if not than return the list contianing object which are different

        :returns: List of objects
        '''

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
        '''
        The method is use to send an email to the responsible person in case any new record (sensitive data is found
        :param email: The email of person you want to send email to
        :type email: str
        :param subject: The subject of the email
        :type subject: str
        :param found_passwords: The new records find
        :type found_passwords: list
        :param found_breaches: The new found breaches
        :type found_breaches: list
        :param found_pastes: The new found pastes
        :type found_pastes: list
        :param found_occurrence_darkweb: The new found darkweb occurrence
        :type found_occurrence_darkweb: list
        '''


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
        logger.info(f'Respective {email} is notified')