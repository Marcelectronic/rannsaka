# Generated by Django 3.2.8 on 2021-10-24 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_alter_stream_notification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='next_run',
            field=models.DateTimeField(null=True),
        ),
    ]
