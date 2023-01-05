from django.contrib import admin
from .models import Project, Tag, Review

admin.site.register([Project, Review, Tag])