# Create your models here.
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video




# Create your models here.

def validate_image(value):
    file_size = value.size
    if file_size > 5242880:
        raise ValidationError("Max size of file is 5MB") 
    else:
        return value





class Profile(models.Model):
    username=models.CharField(max_length=100)
    profilephoto=models.ImageField(upload_to='profilepicture', null=True,blank=True, validators=[validate_image])
    description=models.TextField(max_length=1000, null=True,blank=True)

    def __str__(self):
        return self.username   





class Post(models.Model):
    username=models.CharField(max_length=100)
    photos=models.ImageField(upload_to='photos', null=True,blank=True, validators=[validate_image])
    videos=models.ImageField(upload_to='videos', null=True,blank=True,storage=VideoMediaCloudinaryStorage(),validators=[validate_video])
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







    
    







    

