# Generated by Django 2.2.4 on 2020-11-18 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_X', '0007_auto_20201117_2044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='followed',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='follower',
        ),
        migrations.AddField(
            model_name='profile',
            name='who_follows',
            field=models.ManyToManyField(related_name='_profile_who_follows_+', to='app_X.Profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='you_followed',
            field=models.ManyToManyField(related_name='_profile_you_followed_+', to='app_X.Profile'),
        ),
    ]
