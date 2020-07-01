from django.contrib import admin
from search.models import Messages, Channels, IndexEmail, SearchLog, MonitorEmail, CurrentStatus, DomainEmailStatus, MonitorAsset, Charts, Report, GlobalVar, ApiSearchLog
# Register your models here.

admin.site.register(IndexEmail)
admin.site.register(Channels)
admin.site.register(Messages)
admin.site.register(SearchLog)
admin.site.register(MonitorEmail)
admin.site.register(CurrentStatus)
admin.site.register(MonitorAsset)
admin.site.register(DomainEmailStatus)
admin.site.register(Charts)
admin.site.register(Report)
admin.site.register(GlobalVar)
admin.site.register(ApiSearchLog)