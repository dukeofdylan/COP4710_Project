# Generated by Django 3.1.8 on 2021-04-07 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unievents', '0013_auto_20210407_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(choices=[(5, 'Excellent'), (4, 'Very Good'), (3, 'Average'), (2, 'Poor'), (1, 'Terrible')], db_column='rating'),
        ),
    ]
