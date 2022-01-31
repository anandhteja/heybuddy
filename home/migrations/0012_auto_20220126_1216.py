# Generated by Django 3.2.9 on 2022-01-26 12:16

import cloudinary_storage.storage
from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_post_video_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=100)),
                ('receiver', models.CharField(max_length=100)),
                ('message', models.TextField(blank=True, max_length=1000, null=True)),
                ('chat_photos', models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage, upload_to='chatphotos', validators=[home.models.validate_image])),
                ('uploaded_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='photos',
            field=models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage, upload_to='photos', validators=[home.models.validate_image]),
        ),
        migrations.AlterField(
            model_name='post',
            name='videos',
            field=models.FileField(blank=True, null=True, upload_to='videos', validators=[home.models.validate_video]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profilephoto',
            field=models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage, upload_to='profilepicture', validators=[home.models.validate_image]),
        ),
    ]