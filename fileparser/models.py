from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class FolderSelectInfoModel(models.Model):
    folder_path = models.CharField(max_length=10000, unique=True)
    extensions = ArrayField(models.CharField(max_length=10), blank=True)
    parser = models.CharField(max_length=100)
    start_line = models.PositiveIntegerField(default=0)
    additional_file_path = models.CharField(max_length=10000, blank=True)
    regex_for_additional_file_path = models.CharField(max_length=255, blank=True)
    additional_fields = ArrayField(models.CharField(max_length=100), blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.folder_path


class FileReadInfoModel(models.Model):
    folder = models.ForeignKey(FolderSelectInfoModel, on_delete=models.CASCADE)
    length = models.PositiveIntegerField()
    order = ArrayField(models.CharField(max_length=100))
    delimeter = ArrayField(models.CharField(max_length=100), default=list)
    file_name = models.CharField(max_length=150, blank=True)
    file_name_regex = models.NullBooleanField(default=False)
    start_line = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.folder.folder_path