# Create your models here.
from email.policy import default
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from cloudinary_storage.storage import MediaCloudinaryStorage





# Create your models here.

def validate_image(value):
    file_size = value.size
    if file_size > 5242880:
        raise ValidationError("Max size of file is 5MB") 
    else:
        return value


def validate_video(value):
    file_size = value.size
    if file_size > 52428800:
        raise ValidationError("Max size of file is 5MB") 
    else:
        return value





class Profile(models.Model):
    username=models.CharField(max_length=100)
    profilephoto=models.ImageField(upload_to='profilepicture', null=True,blank=True, storage=MediaCloudinaryStorage, validators=[validate_image])
    description=models.TextField(max_length=1000, null=True,blank=True)

    def __str__(self):
        return self.username   





class Post(models.Model):
    username=models.CharField(max_length=100)
    photos=models.ImageField(upload_to='photos', null=True,blank=True, storage=MediaCloudinaryStorage, validators=[validate_image])
    videos=models.FileField(upload_to='videos', null=True,blank=True, validators=[validate_video])
    video_description=models.TextField(max_length=1000, null=True,blank=True)
    description=models.TextField(max_length=1000, null=True,blank=True)
    status=models.TextField(max_length=1000, null=True,blank=True)
    uploaded_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.username



class Comment(models.Model):
    username=models.CharField(max_length=100)
    postid=models.IntegerField()
    comment=models.CharField(max_length=1000)
    uploaded_on=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username






class Chat(models.Model):
    unique=models.CharField(max_length=200,default='SOME STRING',)
    sender=models.CharField(max_length=100)
    receiver=models.CharField(max_length=100)
    message=models.TextField(max_length=1000, null=True,blank=True)
    chat_photos=models.ImageField(upload_to='chatphotos', null=True,blank=True, storage=MediaCloudinaryStorage, validators=[validate_image])
    uploaded_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.unique

    
    


class Follow(models.Model):
    follower=models.CharField(max_length=100)
    following=models.CharField(max_length=100)


class Chatbackground(models.Model):
    username=models.CharField(max_length=100)
    image=models.ImageField(upload_to='chatbackground', null=True,blank=True, storage=MediaCloudinaryStorage)
    def __str__(self):
        return self.username


class Privateaccount(models.Model):
    username=models.CharField(max_length=100)
    def __str__(self):
        return self.username 


    
class Privatefollow(models.Model):
    requester=models.CharField(max_length=100)
    requesting=models.CharField(max_length=100)
    def __str__(self):
        return self.requester



class Temporarynotification(models.Model):
    sender=models.CharField(max_length=100)
    receiver=models.CharField(max_length=100)
    message=models.TextField(max_length=1000, null=True,blank=True)
    chat_photos=models.TextField(max_length=1000, null=True,blank=True)
    uploaded_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.receiver


class Chatblock(models.Model):
    blocked_user=models.CharField(max_length=100)
    blocked_by=models.CharField(max_length=100)


class Likes(models.Model):
    postid=models.IntegerField()
    liked_by=models.CharField(max_length=100)
    def __str__(self):
        return self.liked_by



class Likefollowcommentnoti(models.Model):
    postid=models.IntegerField(null=True, blank=True)
    username=models.CharField(max_length=100,null=True, blank=True)
    liked_by=models.CharField(max_length=100,null=True, blank=True)
    commented_by=models.CharField(max_length=100,null=True, blank=True)
    followed_by=models.CharField(max_length=100,null=True, blank=True)
    comment=models.CharField(max_length=1000, null=True, blank=True)
    uploaded_on=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username





class Contactdeveloper(models.Model):
    username=models.CharField(max_length=100,default='')
    name=models.CharField(max_length=100,default='')
    email=models.CharField(max_length=100,default='')
    issue=models.TextField(max_length=1000,default='')
    photos=models.ImageField(upload_to='contactdeveloper', null=True,blank=True, storage=MediaCloudinaryStorage, validators=[validate_image])
    def __str__(self):
        return self.username



class Verifiedaccounts(models.Model):
    username=models.CharField(max_length=100,default='')
    def __str__(self):
        return self.username





#groups

class Creategroup(models.Model):
    group_name=models.CharField(max_length=100,default='')
    group_photo=models.ImageField(upload_to='group_photo',null=True, storage=MediaCloudinaryStorage, validators=[validate_image])

    group_description=models.CharField(max_length=1000, default='')
    created_by=models.CharField(max_length=100,default='')
    created_on=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.group_name


class Grouppeople(models.Model):
    group_id=models.IntegerField()
    group_name=models.CharField(max_length=100,default='')
    username=models.CharField(max_length=100,default='')
    
    added_on=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.group_name
        


class Groupsendmessages(models.Model):
    group_id=models.IntegerField()
    sender=models.CharField(max_length=100,default='')
    message=models.CharField(max_length=1000)
    sent_on=models.DateTimeField(auto_now_add=True)
    added_left=models.IntegerField(null=True,blank=True)
    
    


