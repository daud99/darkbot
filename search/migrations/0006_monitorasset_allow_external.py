# Generated by Django 2.2.10 on 2020-07-01 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_auto_20200701_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitorasset',
            name='allow_external',
            field=models.BooleanField(default=False),
        ),
    ]
