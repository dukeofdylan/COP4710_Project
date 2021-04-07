# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_superadmin = models.BooleanField(default=False, null=False)
    university = models.ForeignKey(
        "unievents.university", on_delete=models.DO_NOTHING, related_name="students", null=True
    )
    admin_at: models.Manager

    def is_admin(self, rso_id: int):
        return bool(self.admin_at.filter(pk=rso_id))
