# Generated by Django 3.1.5 on 2021-04-08 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_auto_20210408_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='liked_posts',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liked_posts', to='network.post'),
        ),
    ]