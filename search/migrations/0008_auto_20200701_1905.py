# Generated by Django 2.2.10 on 2020-07-01 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0007_currentassetstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitorasset',
            name='asset_type',
            field=models.CharField(default='domain', max_length=50),
        ),
    ]
