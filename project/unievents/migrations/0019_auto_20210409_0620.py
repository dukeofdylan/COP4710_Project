# Generated by Django 3.1.8 on 2021-04-09 06:20

from django.db import migrations, models
import unievents.models


class Migration(migrations.Migration):

    dependencies = [
        ('unievents', '0018_auto_20210409_0616'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(db_column='text')),
                ('events', models.ManyToManyField(related_name='tags', to='unievents.Event')),
            ],
            options={
                'db_table': 'tag',
            },
            bases=(unievents.models.GetFieldsMixin, models.Model),
        ),
        migrations.AlterModelTable(
            name='comment',
            table='comment',
        ),
        migrations.DeleteModel(
            name='Event_tag',
        ),
    ]