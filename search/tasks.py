from __future__ import absolute_import, unicode_literals
from celery import shared_task
from adminpanel import views
from search.api import views as sv
#from search.darkbot.common.push_to_db import move_email_pass_to_db
@shared_task
def creatingEmailMonitoringReport(file,userid):
    views.handle_uploaded_file(file, userid)
    return "returning from creatingemailmonitoring"

@shared_task
def creatingDomainMonitoringReport(domain, userid, email):
    sv.darkbotDomainReport(domain, userid, email)
    return  "returing form creatingdomainmonitoringreport"

@shared_task
def createEmailReport(fileid):
    sv.report(fileid)
    return "email report generated"

@shared_task
def createDomainReport(userid):
    sv.reportDomain(userid)
    return "domain report generated"

@shared_task
def saveLog(type,query, userid, username, useremail):
    sv.storeApiLog(type, query, userid, username, useremail)

@shared_task
def saveData(res):
    sv.storeInDb(res)


@shared_task
def processUploadEmailFileCreateReport(emails, userid, fileid, uploaderemail, starttime):
    sv.celeryEmailReport(emails, userid, fileid, uploaderemail, starttime)
    return "returning from creatingemailmonitoring"

@shared_task
def processDomainCreateReport(domain, userid, pdf_filename, starttime):
    sv.celerySingleDomainReport(domain, userid, pdf_filename, starttime)
    return "returning celerySingleDomainReport"

@shared_task
def createReportForRegexWildcard(obj):
    sv.createReportForQuery(obj)
    return "returning createReportForRegexWildcard"
