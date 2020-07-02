from django.contrib import admin
from search.models import Messages, Channels, IndexEmail, SearchLog, MonitorEmail,MonitorAsset, Charts, Report, GlobalVar, ApiSearchLog, CurrentAssetStatus
# Register your models here.

admin.site.register(IndexEmail)
admin.site.register(Channels)
admin.site.register(Messages)
admin.site.register(SearchLog)
admin.site.register(MonitorEmail)
admin.site.register(MonitorAsset)
admin.site.register(Charts)
admin.site.register(Report)
admin.site.register(GlobalVar)
admin.site.register(ApiSearchLog)
admin.site.register(CurrentAssetStatus)