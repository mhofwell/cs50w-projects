# Generated by Django 3.1.5 on 2021-04-08 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_auto_20210408_2205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='liked_posts',
        ),
        migrations.AddField(
            model_name='likes',
            name='liked_posts',
            field=models.ManyToManyField(default=None, related_name='liked_posts', to='network.Post'),
        ),
    ]
