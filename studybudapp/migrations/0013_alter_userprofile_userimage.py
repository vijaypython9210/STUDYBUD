# Generated by Django 3.2.25 on 2024-10-06 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studybudapp', '0012_auto_20241006_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='userImage',
            field=models.ImageField(blank=True, upload_to='users'),
        ),
    ]