from jsonfield import JSONField
from django.db import models
from datetime import datetime
from accounts.models import User

# Create your models here.

class SearchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # which user performed the search
    type = models.CharField(max_length=255) # which search type performed
    search_term = models.CharField(max_length=1000) # what is searched
    search_time = models.DateTimeField(default=datetime.now, blank=True) # the time search is performed

    def __str__(self):
        return self.search_term


class ApiSearchLog(models.Model):
    userid = models.CharField(max_length=255, default="") # which user performed the search
    username = models.CharField(max_length=255, default="") # which user performed the search
    useremail = models.CharField(max_length=255, default="") # which user performed the search
    type = models.CharField(max_length=255, default="") # which search type performed
    search_term = models.CharField(max_length=1000, default="") # what is searched
    search_time = models.DateTimeField(default=datetime.now, blank=True) # the time search is performed

    def __str__(self):
        return self.search_term

class IndexEmail(models.Model):
    email = models.EmailField()
    channel_name = models.CharField(max_length=200)
    channel_url = models.CharField(max_length=10000)

    def __str__(self):
        return self.email

class Channels(models.Model):
    channel_name = models.CharField(max_length=200)
    channel_url = models.CharField(max_length=10000)
    channel_index_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.channel_name

class Messages(models.Model):
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField()
    sender_message = models.TextField()
    msg_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.sender_email

class MonitorEmail(models.Model):
    email = models.CharField(max_length=50, default='')
    userid = models.CharField(max_length=255, default='')
    fileid = models.CharField(max_length=255, default='')
    start_date = models.DateTimeField(default=datetime.now, blank=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fileid', 'userid', 'email'], name='uniqueness constraints')
        ]

    def __str__(self):
        return self.email

class CurrentStatus(models.Model):
    email = models.ForeignKey(MonitorEmail, on_delete=models.CASCADE, related_name='em')
    ghostfrpasswords = JSONField(blank=True)
    breaches = JSONField(blank=True)
    no_of_paste = models.PositiveIntegerField(blank=True)
    # emailsindb = JSONField(blank=True)
    indexemails = JSONField(blank=True)

class MonitorAsset(models.Model):
    asset = models.CharField(max_length=50, default='')
    support_email = models.EmailField(default="daudahmed@zoho.com")
    userid = models.CharField(max_length=255, default='')
    fileid = models.CharField(max_length=255, default='')
    allow_monitoring = models.BooleanField(default=True)
    asset_type = models.CharField(max_length=50, default='Domain')
    asset_status = models.CharField(max_length=50, default='In Active')
    asset_verify = models.BooleanField(default=False)
    allow_external = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.asset

class DomainEmailStatus(models.Model):
    email = models.EmailField(unique=True)
    domain = models.ForeignKey(MonitorAsset, on_delete=models.CASCADE)
    passwords = JSONField(blank=True)
    darknet_occurrences = JSONField(blank=True)
    def __str__(self):
        return self.email

class CurrentAssetStatus(models.Model):
    asset = models.ForeignKey(MonitorAsset, on_delete=models.CASCADE, related_name='asset_name')
    records = JSONField(blank=True)

    def __str__(self):
        return self.asset.asset


class Charts(models.Model):
    chart_name = models.CharField(max_length=255)
    chart_file = models.CharField(max_length=255)
    chart_user = models.CharField(max_length=255)

    def __str__(self):
        return self.chart_name

class Report(models.Model):
    fileid = models.CharField(max_length=50)
    userid = models.CharField(max_length=50)
    report_type = models.CharField(max_length=50)
    status = models.CharField(default="pending", max_length=100)
    request_date = models.DateTimeField(default=datetime.now, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.fileid

class GlobalVar(models.Model):
    type = models.CharField(max_length=50, default='email', unique=True)
    monitoring = models.BooleanField(default=False)

