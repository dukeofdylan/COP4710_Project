# Generated by Django 3.1.7 on 2021-04-03 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('unievents', '0003_auto_20210402_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event_location',
            name='event',
        ),
        migrations.RemoveField(
            model_name='event_location',
            name='location',
        ),
        migrations.RemoveField(
            model_name='has_tag',
            name='event',
        ),
        migrations.RemoveField(
            model_name='has_tag',
            name='event_tag',
        ),
        migrations.RemoveField(
            model_name='organizes',
            name='event',
        ),
        migrations.RemoveField(
            model_name='organizes',
            name='rso',
        ),
        migrations.RemoveField(
            model_name='rated',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='rated',
            name='user',
        ),
        migrations.RemoveField(
            model_name='registeredat',
            name='rso',
        ),
        migrations.RemoveField(
            model_name='registeredat',
            name='university',
        ),
        migrations.AddField(
            model_name='comment',
            name='event',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='unievents.event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='accounts.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='unievents.location'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='rso',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='unievents.rso'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event_tag',
            name='event',
            field=models.ManyToManyField(related_name='tags', to='unievents.Event'),
        ),
        migrations.AddField(
            model_name='rso',
            name='members',
            field=models.ManyToManyField(related_name='rso_memberships', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rso',
            name='university',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='rsos', to='unievents.university'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(db_column='rating', null=True),
        ),
        migrations.AlterField(
            model_name='rso',
            name='description',
            field=models.TextField(db_column='description', default=''),
        ),
        migrations.DeleteModel(
            name='Commented_on',
        ),
        migrations.DeleteModel(
            name='Event_location',
        ),
        migrations.DeleteModel(
            name='Has_Tag',
        ),
        migrations.DeleteModel(
            name='Organizes',
        ),
        migrations.DeleteModel(
            name='Rated',
        ),
        migrations.DeleteModel(
            name='Registeredat',
        ),
    ]
