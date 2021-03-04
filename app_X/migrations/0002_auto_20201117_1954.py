# Generated by Django 2.2.4 on 2020-11-18 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_X', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followed',
            field=models.ManyToManyField(related_name='_profile_followed_+', to='app_X.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(related_name='_profile_followers_+', to='app_X.Profile'),
        ),
    ]
