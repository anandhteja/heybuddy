# Create your models here.
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