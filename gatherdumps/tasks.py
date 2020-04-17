from __future__ import absolute_import, unicode_literals
from celery import shared_task
from gatherdumps.scripts.celery_related import crawler_handlers
@shared_task
def crawl_markets(identity):
    if (identity==11):
        crawler_handlers.collect_BrocardDumps(identity)
    elif (identity==12):
        crawler_handlers.collect_BrocardCvvs(identity)
    elif (identity==21):
        crawler_handlers.collect_MeccaDumps(identity)
    elif (identity==22):
        crawler_handlers.collect_MeccaCvvs(identity)
    elif (identity==43):
        crawler_handlers.collect_emails_over_forums(identity)
    elif (identity==53):
        crawler_handlers.daud_collect_email_passwords(300)
    elif (identity==54):
        crawler_handlers.daud_collect_email_passwords(302)
    return "Done Data Gathering"