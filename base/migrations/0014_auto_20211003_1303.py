# Generated by Django 3.2.6 on 2021-10-03 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_auto_20211003_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='notification_cc',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='stream',
            name='notification_to',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
