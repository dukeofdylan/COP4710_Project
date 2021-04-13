# Generated by Django 3.1.8 on 2021-04-07 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unievents', '0014_auto_20210407_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event_tag',
            name='event_tag_name',
        ),
        migrations.AddField(
            model_name='event_tag',
            name='text',
            field=models.TextField(db_column='text', default=None),
            preserve_default=False,
        ),
    ]
