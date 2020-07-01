from __future__ import absolute_import, unicode_literals
from celery import shared_task
from fileparser.scripts.main import main
from search.darkbot.monitoring import main

@shared_task
def Monitoring(type):
    main.main(type)
    return "email monitoring returning"

@shared_task
def startMainForFileParser(folder_path):
    main(folder_path)
    return "returining from file parser main"