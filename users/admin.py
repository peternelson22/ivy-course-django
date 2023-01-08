from django.contrib import admin
from .models import Profile, Skill, Message

admin.site.register([Profile, Skill, Message])