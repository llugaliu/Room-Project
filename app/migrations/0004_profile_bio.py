# Generated by Django 4.2.5 on 2023-09-12 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_profile_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
