# Generated by Django 3.1.8 on 2021-04-07 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unievents', '0016_auto_20210407_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='university',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='unievents.university'),
            preserve_default=False,
        ),
    ]