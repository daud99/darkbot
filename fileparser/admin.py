from django.contrib import admin
from fileparser.models import FolderSelectInfoModel, FileReadInfoModel

# Register your models here.

admin.site.register(FileReadInfoModel)
admin.site.register(FolderSelectInfoModel)