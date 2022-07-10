from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile

def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
        )
    else:
        user = instance
        full_name = user.first_name + ' ' + user.last_name
        profile = Profile.objects.filter(username__exact=user.username).update(
            user=user,
            username=user.username,
            email=user.email,
            name=full_name,
        )

post_save.connect(create_profile, sender=User)


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user_deleted = User.objects.filter(username__exact=user).delete()
