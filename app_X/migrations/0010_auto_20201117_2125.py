# Generated by Django 2.2.4 on 2020-11-18 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_X', '0009_auto_20201117_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(related_name='who_follows', to='app_X.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(related_name='you_followed', to='app_X.Profile'),
        ),
    ]
