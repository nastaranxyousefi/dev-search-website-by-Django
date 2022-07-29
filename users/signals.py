from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from .models import Profile

def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        full_name = user.first_name + ' ' + user.last_name
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            name=full_name,
            email=user.email,
        )


post_save.connect(create_profile, sender=User)

def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        try:
            user.first_name = profile.name.split()[0]
        except:
            pass

        try:
            user.last_name = profile.name.split()[1]
        except:
            pass
        user.username = profile.username
        user.email = profile.email
        user.save()

post_save.connect(update_user, sender=Profile)


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user_deleted = User.objects.filter(username__exact=user).delete()
