from django.contrib import admin
from home.models import Profile, Post, Comment, Chat, Follow
from django.contrib.auth.models import User







# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Chat)

class Followadmin(admin.ModelAdmin):
    list_display=['follower', 'following']

admin.site.register(Follow, Followadmin)