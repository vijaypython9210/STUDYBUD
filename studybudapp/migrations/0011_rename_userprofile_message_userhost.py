# Generated by Django 3.2.25 on 2024-10-01 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studybudapp', '0010_rename_user_message_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='userProfile',
            new_name='userhost',
        ),
    ]
