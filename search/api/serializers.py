from rest_framework import serializers
from search.models import IndexEmail, MonitorDomain, Report
from gatherdumps.models import CardCvv, CardDump, Email_passwords

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['fileid', 'userid', 'report_type', 'status', 'request_date', "create_date"]

class MonitorDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorDomain
        fields = ['id', 'domain', 'userid', 'asset_type', 'asset_status', 'asset_verify']


class Email_passwordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email_passwords
        fields = ['email', 'password', 'source', 'username', 'hash', 'ipaddress', 'phonenumber']

class IndexEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexEmail
        fields = ['email', 'channel_name', 'channel_url']

class CardCvvSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardCvv
        fields = ['bin_no','country','base','bank','card_type','card_category','expiry','name','refund','card_mark','city','state','zip_no','source','date','price']


class CardDumpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardDump
        fields = ['bin_no', 'track', 'carr', 'card_type', 'card_category', 'refund', 'card_mark', 'bank', 'country', 'dumped_in', 'base', 'quantity', 'price', 'source', 'date']





