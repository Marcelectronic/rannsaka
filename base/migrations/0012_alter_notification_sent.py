# Generated by Django 3.2.6 on 2021-10-03 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='sent',
            field=models.DateTimeField(),
        ),
    ]
