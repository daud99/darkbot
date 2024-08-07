# Generated by Django 2.2.10 on 2020-05-28 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gatherdumps', '0007_auto_20200415_0819'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='email_passwords',
            name='email password source unique',
        ),
        migrations.RemoveConstraint(
            model_name='email_passwords',
            name='username password source unique',
        ),
        migrations.RemoveConstraint(
            model_name='email_passwords',
            name='username  email password source unique',
        ),
        migrations.AlterField(
            model_name='email_passwords',
            name='domain',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='email_passwords',
            name='email',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='email_passwords',
            name='hash',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='email_passwords',
            name='ipaddress',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='email_passwords',
            name='phonenumber',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
