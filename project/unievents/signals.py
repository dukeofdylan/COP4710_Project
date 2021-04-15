from accounts.models import User
from unievents.models import University
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction


@receiver(post_save, sender=University)
def university_post_save(sender, instance, created: bool, update_fields, *args, **kwargs):
    if created or (update_fields and "email_domain" in update_fields):
        students = User.objects.filter(email__endswith=instance.email_domain)
        if students:
            with transaction.atomic():
                for student in students:
                    student.university_id = instance.university_id
                    student.save()
                instance.student_count += len(students)  # FIXME: Make it a fricking view! (in db terms)
                instance.save()
