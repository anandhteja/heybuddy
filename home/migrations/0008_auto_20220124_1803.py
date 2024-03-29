# Generated by Django 3.2.9 on 2022-01-24 18:03

from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_profile_profilephoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='videos',
            field=models.FileField(blank=True, null=True, upload_to='videos'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profilephoto',
            field=models.ImageField(blank=True, null=True, upload_to='profilepicture', validators=[home.models.validate_image]),
        ),
    ]
