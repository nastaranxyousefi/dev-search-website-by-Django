from django.db import models
import uuid
from django.urls import reverse

from users.models import Profile


class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='project_cover/default.jpg', upload_to='project_cover/')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_code = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total']

    @property
    def get_vote_count(self):
        reviews = self.review_set.all()
        up_vote = reviews.filter(value='up').count()
        total_vote = reviews.count()

        ratio = (up_vote / total_vote) * 100
        self.vote_ratio = ratio
        self.vote_total = total_vote
        self.save()


    @property
    def image_URL(self):
        try:
            url = self.featured_image.url
        except:
            url = 'http://127.0.0.1:8000/images/project_cover/default.jpg'
        return url


class Review(models.Model):
    VOTE_CHOICES = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner= models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=50, choices=VOTE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)


    class Meta:
        unique_together = [['owner', 'project']]


    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name
