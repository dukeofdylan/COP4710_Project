# TODO: Add unique constraints
from django.db import models
from accounts.models import User
from multiselectfield import MultiSelectField

from pathlib import Path


class GetFieldsMixin:
    def get_fields(self: models.Model):  # type: ignore
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]


class Location(GetFieldsMixin, models.Model):
    location_id = models.AutoField(db_column="location_id", primary_key=True)
    longitude = models.FloatField(db_column="longitude", blank=False, null=False)
    latitude = models.FloatField(db_column="latitude", blank=False, null=False)
    image = models.ImageField(db_column="image", blank=False, null=False)

    class Meta:
        db_table = "location"
        unique_together = ("longitude", "latitude")


def uni_image_upload_to(instance, filename):
    return f"university/{instance.name}{Path(filename).suffix}"


class University(GetFieldsMixin, models.Model):
    university_id = models.AutoField(db_column="university_id", primary_key=True)
    # TODO: make it a view or make a trigger for it
    student_count = models.IntegerField(db_column="student_count", blank=True, null=False)
    name = models.TextField(db_column="name", blank=False, null=False)
    description = models.TextField(db_column="description", blank=True, null=False, default="")
    avatar_image = models.ImageField(db_column="avatar_image", blank=False, null=False, upload_to=uni_image_upload_to)
    email_domain = models.TextField(db_column="email_domain", blank=False, null=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False, null=False)
    max_avatar_size = 5 * 1024 * 1024
    students: "models.manager.RelatedManager"

    class Meta:
        db_table = "university"


class RSO(GetFieldsMixin, models.Model):
    rso_id = models.AutoField(db_column="rso_id", primary_key=True)
    name = models.TextField(db_column="name", blank=False, null=False)
    description = models.TextField(db_column="description", blank=True, null=False, default="")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name="admin_at")
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=False, null=False, related_name="rsos")
    members = models.ManyToManyField(User, related_name="rso_memberships")

    class Meta:
        db_table = "rso"


class Event(GetFieldsMixin, models.Model):
    class PrivacyLevel(models.IntegerChoices):
        Public = 1
        University_Private = 2
        RSO_Private = 3

    class Frequency(models.TextChoices):
        Once = "ONCE"
        Daily = "DAILY"
        Weekly = "WEEKLY"
        # Not implemented yet
        # Monthly = "MONTHLY"
        # Yearly = "YEARLY"

    class Weekday(models.TextChoices):
        Monday = "MO"
        Tuesday = "TU"
        Wednesday = "WE"
        Thursday = "TH"
        Friday = "FR"
        Saturday = "SA"
        Sunday = "SU"

    event_id = models.AutoField(db_column="event_id", primary_key=True)
    summary = models.TextField(db_column="summary")
    privacy_level = models.IntegerField(
        db_column="privacy_level",
        null=False,
        blank=False,
        choices=PrivacyLevel.choices,
        default=PrivacyLevel.Public,
    )
    description = models.TextField(db_column="description", blank=True, null=False, default="")
    phone = models.TextField(db_column="phone", blank=False, null=False)
    email = models.TextField(db_column="email", blank=False, null=False)
    dtstart = models.DateTimeField(db_column="dtstart", blank=False, null=False)
    dtend = models.DateTimeField(db_column="dtend", blank=True)
    freq = models.TextField(
        db_column="freq",
        null=False,
        blank=True,
        choices=Frequency.choices,
        default=Frequency.Once,
        verbose_name="frequency",
    )
    until = models.DateField(db_column="until", blank=True, null=True)
    byday = MultiSelectField(
        db_column="byday",
        blank=True,
        null=True,
        choices=Weekday.choices,
        verbose_name="Repeat on",
    )
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False, null=False)
    rso = models.ForeignKey(RSO, on_delete=models.CASCADE, related_name="events", blank=False, null=False)
    tags: "models.manager.RelatedManager"

    class Meta:
        db_table = "event"

    def formatted_tags(self):
        return ", ".join(t.text for t in self.tags.all())


class Comment(GetFieldsMixin, models.Model):
    class Rating(models.IntegerChoices):
        Excellent = 5
        Very_Good = 4
        Average = 3
        Poor = 2
        Terrible = 1

    comment_id = models.AutoField(db_column="comment_id", primary_key=True)
    postdate = models.DateTimeField(db_column="postdate", auto_now_add=True, blank=False, null=False)
    text = models.TextField(db_column="text", blank=False, null=False)
    rating = models.IntegerField(db_column="rating", blank=False, null=False, choices=Rating.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", blank=False, null=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments", blank=False, null=False)

    class Meta:
        db_table = "comment"


class Event_tag(GetFieldsMixin, models.Model):
    event_tag_id = models.AutoField(db_column="event_tag_id", primary_key=True)
    text = models.TextField(db_column="text", blank=False, null=False)
    events = models.ManyToManyField(Event, related_name="tags", blank=False)

    class Meta:
        db_table = "event_tag"
