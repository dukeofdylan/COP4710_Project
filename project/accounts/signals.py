from accounts.models import User
from unievents.models import University
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created: bool, update_fields, *args, **kwargs):
    if created or (update_fields and "email" in update_fields):
        email_domain = instance.email.split("@")[1]
        unis = University.objects.filter(email_domain=email_domain)
        if unis:
            uni = unis[0]
            with transaction.atomic():
                instance.university_id = uni.id
                instance.save()
                uni.student_count += 1
                uni.save()
