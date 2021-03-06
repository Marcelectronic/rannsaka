# Generated by Django 3.2.6 on 2021-10-03 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_notification_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='notification_cc',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='stream',
            name='notification_to',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='stream',
            name='notification_type',
            field=models.CharField(choices=[('None', 'None'), ('Every Run', 'Every Run'), ('Every Run - Only when errors', 'Every Run - Only when errors'), ('Once per Day', 'Once per Day'), ('Once per Day - Only when errors', 'Once per Day - Only when errors'), ('Once per Week Summary', 'Once per Week Summary')], default='None', max_length=50),
        ),
    ]
