from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    username = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to='profiles/',
                         default='profiles/user-default.png')
    social_github = models.CharField(max_length=500, blank=True, null=True)
    social_linkedin = models.CharField(max_length=500, blank=True, null=True)
    social_website = models.CharField(max_length=500, blank=True, null=True)
    social_twitter = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['-created',]

    @property
    def image_URL(self):
        try:
            url = self.profile_image.url
        except:
            url = 'http://127.0.0.1:8000/images/profiles/user-default.png'
        return url


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=False, related_name='messages')
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=250, null=True, blank=True)
    subject = models.CharField(max_length=500, null=True, blank=True)
    body = models.TextField(blank=False, null=False)
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
