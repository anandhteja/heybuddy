# Generated by Django 3.2.9 on 2022-02-18 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_groupsendmessages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupsendmessages',
            name='sent_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]