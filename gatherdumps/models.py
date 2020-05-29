from django.db import models
from django.db.models import Q
from datetime import datetime

class CardDump(models.Model):
    bin_no = models.CharField(max_length=6)
    track = models.CharField(max_length=20)
    carr = models.CharField(max_length=255)
    card_type = models.CharField(max_length=50)
    card_category = models.CharField(max_length=50)
    refund = models.CharField(max_length=10)
    card_mark = models.CharField(max_length=20)
    bank = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    dumped_in = models.CharField(max_length=50)
    base = models.CharField(max_length=100)
    quantity = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    source = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.bin_no


class CardCvv(models.Model):
    bin_no = models.CharField(max_length=6)
    card_type = models.CharField(max_length=100)
    card_category = models.CharField(max_length=100)
    refund = models.CharField(max_length=10)
    card_mark = models.CharField(max_length=20)
    expiry = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_no = models.CharField(max_length=50)
    bank = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    base = models.CharField(max_length=100)
    price = models.CharField(max_length=255)
    source = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.bin_no


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, default="Unknown")
    alpha3_code = models.CharField(max_length=3, default="Test")

    def __str__(self):
        return self.name


class Email_passwords(models.Model):
    email = models.CharField(max_length=50, null=True)
    password = models.CharField(db_index=True, max_length=40, null=True)
    source = models.CharField(default='unknown', max_length=150, null=True)
    domain = models.CharField(max_length=50, null=True)
    before_at = models.CharField(max_length=255, null=True)
    username = models.CharField(db_index=True, max_length=150, null=True)
    hash = models.CharField(max_length=255, null=True)
    ipaddress = models.CharField(max_length=50, null=True)
    phonenumber = models.CharField(max_length=100, null=True)

    class Meta:
        # constraints = [
        #     models.UniqueConstraint(fields=['email', 'password', 'source'],
        #                             condition=Q(email__isnull=False, username__isnull=True),
        #                             name='email password source unique'),
        #     models.UniqueConstraint(fields=['username', 'password', 'source'],
        #                             condition=Q(username__isnull=False, email__isnull=True),
        #                             name='username password source unique'),
        #     models.UniqueConstraint(fields=['username', 'email', 'password', 'source'],
        #                             condition=Q(username__isnull=False, email__isnull=False),
        #                             name='username  email password source unique')
        # ]

        index_together = [
            ("domain", "before_at"),
        ]

    def __str__(self):
        if self.email != None:
            return self.email
        elif self.username != None:
            return self.username


class CardMarket(models.Model):
    # id = models.AutoField(primary_key=True, null=False, blank=False, default=1)
    name = models.CharField(max_length=20, unique=True)
    url = models.URLField(max_length=50, unique=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    require_credetials = models.BooleanField(default=True)
    require_captcha = models.BooleanField(default=True)
    market_identity = models.IntegerField(unique=True, primary_key=True)

    def __str__(self):
        return self.name


class Checkpoint(models.Model):
    name = models.CharField(max_length=20, unique=True, default="Test Checkpoint")

    next_index = models.PositiveIntegerField(default=0)
    Checkpoint_identity = models.IntegerField(unique=True,
                                              choices=((11, "Brocard Dumps"), (12, "Brocard CVVs"),
                                                       (21, "MeccaDumps Dumps"), (22, "MeccaDumps CVVs"),
                                                       (31, "Franklins Dumps"), (32, "Franklins CVVs"),
                                                       (1001, "Indexed Forums"),
                                                       (1002, "Emails & Pass")))

    def __str__(self):
        return self.name


class CrawlerAccess(models.Model):
    name = models.CharField(max_length=50, default="Descriptive Name")
    Access_identity = models.IntegerField(unique=True,
                                          choices=((100, "Dump Cvv Collectors"), (200, "Indexed Forums"),
                                                   (300, "Emails & Pass"),
                                                   (400, "Authorization to Control Dynamic Crawler")))
    authorize_access = models.BooleanField(default=False)
    authorize_cancel = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class FilePath(models.Model):
    source = models.CharField(max_length=50, default="source")
    path = models.CharField(max_length=255, default="Give a path")
    status = models.CharField(max_length=255, default="never started")
    break_point = models.CharField(max_length=50, default=':')
    identifier = models.IntegerField(unique=True, default=0)

    def __str__(self):
        return self.source


class Crawler_Breaker(models.Model):
    Description = models.CharField(max_length=50, default="Descriptive Name")
    breaker = models.BooleanField(default=False)
    identifier = models.IntegerField(unique=True, default=0)

    def __str__(self):
        return self.Description






