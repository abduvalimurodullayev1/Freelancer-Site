from apps.users.models import Profile
from apps.users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(f"User {instance.username} created with type {instance.user_type}")
        if instance.user_type == 'freelancer':
            Profile.objects.create(user=instance)
            print("FreelancerProfile created")
        elif instance.user_type == 'employer':
            Profile.objects.create(user=instance)
            print("EmployerProfile created")
