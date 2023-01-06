from django.db import models
import uuid
from users.models import Profile

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_img = models.ImageField(null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_code = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project'
        ordering = ['-vote_ratio', '-vote_total', 'title']

    def __str__(self) -> str:
        return self.title

    @property
    def getvotecount(self):
        reviews = self.review_set.all()
        upvotes = reviews.filter(value='up').count()
        total_votes = reviews.count()

        ratio = (upvotes / total_votes) * 100
        self.vote_total = total_votes
        self.vote_ratio = ratio
        self.save()

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset


class Review(models.Model):

    VOTE_TYPE = (
        ('up', ' Up Vote'),
        ('down', ' Down Vote'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE) 
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'review'
        unique_together = [['owner', 'project']]

    def __str__(self) -> str:
        return self.value

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tag'

    def __str__(self) -> str:
        return self.name