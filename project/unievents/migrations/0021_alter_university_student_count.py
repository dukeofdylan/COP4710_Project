# Generated by Django 3.2 on 2021-04-13 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unievents', '0020_auto_20210409_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='student_count',
            field=models.IntegerField(blank=True, db_column='student_count', default=0),
        ),
    ]
