# Generated by Django 3.2.9 on 2022-01-30 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_auto_20220130_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='likefollowcommentnoti',
            name='comment',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
