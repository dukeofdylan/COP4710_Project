# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    google_place_id = models.AutoField(db_column="google_place_id", primary_key=True)  #
    name = models.TextField(db_column="name", null=True)  #
    latitude = models.FloatField(db_column="latitude", blank=True, null=False)  #
    longitude = models.FloatField(db_column="longitude", blank=True, null=False)  #

    class Meta:
        db_table = "location"


class University(models.Model):
    university_id = models.AutoField(db_column="university_id", primary_key=True)  #
    student_count = models.IntegerField(db_column="student_count")  # TODO: make it a view or make a trigger for it
    name = models.TextField(db_column="name", blank=True)  #
    description = models.TextField(db_column="description", blank=True, null=True)  #
    avatar_image = models.TextField(db_column="avatar_image", blank=True, null=True)  # This field type is a guess.
    email_domain = models.TextField(db_column="email_domain")  #

    class Meta:
        db_table = "university"


class University_location(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        db_table = "university_location"


class Super_admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "super_admin"


class Studies_at(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    class Meta:
        db_table = "studies_at"


class RSO(models.Model):
    rso_id = models.AutoField(db_column="rso_id", primary_key=True)  #
    name = models.TextField(db_column="name")  #
    description = models.TextField(db_column="description", null=True)  #
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "rso"


class Registeredat(models.Model):
    rso = models.ForeignKey(RSO, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    class Meta:
        db_table = "registered_at"


class Member_of(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rso = models.ForeignKey(RSO, on_delete=models.CASCADE)

    class Meta:
        db_table = "member_of"


class Event(models.Model):
    event_id = models.AutoField(db_column="event_id", primary_key=True)  #
    summary = models.TextField(db_column="summary")  #
    privacy_level = models.IntegerField(db_column="privacy_level")  #
    description = models.TextField(db_column="description", blank=True, null=True)  #
    phone = models.TextField(db_column="phone", blank=True, null=True)  #
    email = models.TextField(db_column="email", blank=True, null=True)  #
    dtstart = models.DateTimeField(db_column="dtstart", auto_now_add=True)
    dtend = models.DateTimeField(db_column="dtend", auto_now_add=True)
    until = models.DateTimeField(db_column="until", auto_now_add=True)
    rrule = models.TextField(db_column="rrule", null=True)  #

    class Meta:
        db_table = "event"


class Event_location(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        db_table = "event_location"


class Organizes(models.Model):
    rso = models.ForeignKey(RSO, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        db_table = "organizes"


class Comment(models.Model):
    # This field type is a guess.
    comment_postdate = models.DateTimeField(db_column="comment_postdate", primary_key=True, auto_now_add=True)
    text = models.TextField(db_column="text", blank=True)  #
    rating = models.FloatField(db_column="rating", null=True)  #

    class Meta:
        db_table = "comment"


class Commented_on(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        db_table = "commented_on"


class Rated(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    rating = models.IntegerField(db_column="rating")

    class Meta:
        db_table = "rated"


class Event_tag(models.Model):
    event_tag_id = models.AutoField(db_column="event_tag_id", primary_key=True)  #
    event_tag_name = models.TextField(db_column="event_tag_name")  #

    class Meta:
        db_table = "event_tag"


class Has_Tag(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    event_tag = models.ForeignKey(Event_tag, on_delete=models.CASCADE)

    class Meta:
        db_table = "has_tag"