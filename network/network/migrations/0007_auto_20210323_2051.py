# Generated by Django 3.1.5 on 2021-03-23 20:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20210320_1811'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='following',
            new_name='number_of_followers',
        ),
        migrations.RemoveField(
            model_name='userfollowers',
            name='followers',
        ),
        migrations.AddField(
            model_name='userfollowers',
            name='following',
            field=models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]