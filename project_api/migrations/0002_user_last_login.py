# Generated by Django 3.0.3 on 2020-02-08 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
