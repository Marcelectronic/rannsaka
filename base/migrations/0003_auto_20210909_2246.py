# Generated by Django 3.2.6 on 2021-09-09 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20210909_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='parameters',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='module',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Module_template_id', to='base.template'),
        ),
    ]