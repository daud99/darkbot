from __future__ import absolute_import, unicode_literals
from celery import shared_task

from search.darkbot import domain_monitoring
from search.darkbot.monitor import startMonitor
from fileparser.scripts.main import main
@shared_task
def Monitoring(switch):
    startMonitor(switch)
    return "email monitoring returning"

@shared_task
def startDomainMonitoring():
    domain_monitoring.start_domain_monitoring()
    return "start domain monitoring returning"

@shared_task
def stopDomainMonitoring():
    domain_monitoring.stop_domain_monitoring()
    return "stop domain monitoring returning"

@shared_task
def startMainForFileParser(folder_path):
    main(folder_path)
    return "returining from file parser main"