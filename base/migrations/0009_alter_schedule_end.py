# Generated by Django 3.2.6 on 2021-09-22 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_module_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='end',
            field=models.DateTimeField(null=True),
        ),
    ]