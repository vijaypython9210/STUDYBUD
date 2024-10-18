# Generated by Django 3.2.25 on 2024-10-10 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studybudapp', '0015_auto_20241010_1308'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userImage', models.ImageField(blank=True, default='default.jpg', upload_to='user_image/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.AlterField(
            model_name='message',
            name='userhost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studybudapp.userprofile'),
        ),
        migrations.AlterField(
            model_name='room',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='studybudapp.userprofile'),
        ),
    ]
