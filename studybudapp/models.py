from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# User With UserImage
class UserProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    userImage=models.ImageField(upload_to='user_image/',blank=True,null=True)

    def __str__(self):
        return str(self.user)

# Topics
class Topic(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Rooms
class Room(models.Model):
    host=models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True)
    topic=models.ForeignKey(Topic, on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=100)
    description=models.TextField(max_length=250)
    participants=models.ManyToManyField(UserProfile,related_name='participants',blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']

    def __str__(self):
        return self.name

# Comments or Messages
class Message(models.Model):
    userhost=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]


