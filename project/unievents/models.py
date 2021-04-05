# TODO: Add unique constraints
from django.db import models
from django.db.models.manager import Manager
from accounts.models import User
from multiselectfield import MultiSelectField

from pathlib import Path


class GetFieldsMixin:
    def get_fields(self: models.Model):  # type: ignore
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]


class Location(GetFieldsMixin, models.Model):
    location_id = models.AutoField(db_column="location_id", primary_key=True)
    longitude = models.FloatField(db_column="longitude", blank=True, null=False)
    latitude = models.FloatField(db_column="latitude", blank=True, null=False)
    image = models.ImageField(db_column="image", blank=True, null=False)

    class Meta:
        db_table = "location"
        unique_together = ("longitude", "latitude")


def uni_image_upload_to(instance, filename):
    return f"university/{instance.name}{Path(filename).suffix}"


class University(GetFieldsMixin, models.Model):
    university_id = models.AutoField(db_column="university_id", primary_key=True)
    # TODO: make it a view or make a trigger for it
    student_count = models.IntegerField(db_column="student_count", default=0)
    name = models.TextField(db_column="name", blank=True)
    description = models.TextField(db_column="description", blank=True, null=True)
    avatar_image = models.ImageField(db_column="avatar_image", blank=True, null=False, upload_to=uni_image_upload_to)
    email_domain = models.TextField(db_column="email_domain")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=False)
    max_avatar_size = 5 * 1024 * 1024
    students: Manager

    class Meta:
        db_table = "university"


class RSO(GetFieldsMixin, models.Model):
    rso_id = models.AutoField(db_column="rso_id", primary_key=True)
    name = models.TextField(db_column="name")
    description = models.TextField(db_column="description", null=False, default="")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_at")
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=False, related_name="rsos")
    members = models.ManyToManyField(User, related_name="rso_memberships")

    class Meta:
        db_table = "rso"


WEEKDAY_CHOICES = (
    ("MO", "Monday"),
    ("TU", "Tuesday"),
    ("WE", "Wednesday"),
    ("TH", "Thursday"),
    ("FR", "Friday"),
    ("SA", "Saturday"),
    ("SU", "Sunday"),
)


class Event(GetFieldsMixin, models.Model):
    class PrivacyLevel(models.IntegerChoices):
        Public = 1
        University_Private = 2
        RSO_Private = 3

    class Frequency(models.TextChoices):
        Daily = "DAILY"
        Weekly = "WEEKLY"
        Monthly = "MONTHLY"
        Yearly = "YEARLY"

    event_id = models.AutoField(db_column="event_id", primary_key=True)
    summary = models.TextField(db_column="summary")
    privacy_level = models.IntegerField(db_column="privacy_level", null=False, blank=True, choices=PrivacyLevel.choices)
    description = models.TextField(db_column="description", blank=True, null=True)
    phone = models.TextField(db_column="phone", blank=True, null=True)
    email = models.TextField(db_column="email", blank=True, null=True)
    dtstart = models.DateTimeField(db_column="dtstart", blank=True)
    dtend = models.DateTimeField(db_column="dtend", blank=True)
    until = models.DateTimeField(db_column="until", null=True)
    freq = models.TextField(db_column="freq", null=True, choices=Frequency.choices, verbose_name="frequency")
    byday = MultiSelectField(db_column="byday", null=True, choices=WEEKDAY_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=False)
    rso = models.ForeignKey(RSO, on_delete=models.CASCADE, related_name="events", blank=True, null=False)

    class Meta:
        db_table = "event"


class Comment(GetFieldsMixin, models.Model):
    comment_id = models.AutoField(db_column="comment_id", primary_key=True)
    postdate = models.DateTimeField(db_column="postdate", auto_now_add=True)
    text = models.TextField(db_column="text", blank=True)
    rating = models.IntegerField(db_column="rating", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        db_table = "comment"


class Event_tag(GetFieldsMixin, models.Model):
    event_tag_id = models.AutoField(db_column="event_tag_id", primary_key=True)
    event_tag_name = models.TextField(db_column="event_tag_name")
    event = models.ManyToManyField(Event, related_name="tags")

    class Meta:
        db_table = "event_tag"
