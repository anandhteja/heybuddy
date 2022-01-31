from django.contrib import admin
from home.models import Profile, Post, Comment, Chat,Contactdeveloper, Follow,Likefollowcommentnoti, Chatbackground, Privateaccount, Privatefollow, Temporarynotification, Chatblock, Likes
from django.contrib.auth.models import User







# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Chat)

class Followadmin(admin.ModelAdmin):
    list_display=['follower', 'following']

admin.site.register(Follow, Followadmin)

admin.site.register(Chatbackground)
admin.site.register(Privateaccount)
admin.site.register(Privatefollow)

admin.site.register(Temporarynotification)


class Chatbloackadmin(admin.ModelAdmin):
    list_display=['blocked_user', 'blocked_by']

admin.site.register(Chatblock,Chatbloackadmin )

admin.site.register(Likes)
admin.site.register(Likefollowcommentnoti)

admin.site.register(Contactdeveloper)

