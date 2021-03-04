# Generated by Django 2.2.4 on 2020-11-18 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_X', '0010_auto_20201117_2125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.AddField(
            model_name='comment',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_comments', to='app_X.Profile'),
        ),
        migrations.AddField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='app_X.Profile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='disliked',
            field=models.ManyToManyField(related_name='posts_disliked', to='app_X.Profile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='liked',
            field=models.ManyToManyField(related_name='posts_liked', to='app_X.Profile'),
        ),
    ]
