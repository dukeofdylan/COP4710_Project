# Generated by Django 3.1.8 on 2021-04-07 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unievents', '0015_auto_20210407_1554'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event_tag',
            old_name='event',
            new_name='events',
        ),
    ]
