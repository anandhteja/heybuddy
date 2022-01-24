# Generated by Django 3.2.9 on 2022-01-18 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_delete_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('postid', models.IntegerField()),
                ('comment', models.CharField(max_length=1000)),
            ],
        ),
    ]
