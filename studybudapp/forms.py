from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Room,Topic,UserProfile

class CreteRoomForm(ModelForm):
    topics=Topic.objects.all()
    topic=forms.ModelChoiceField(
        queryset=topics,
        label="Topic Name",widget=forms.Select(attrs={
            'class':'form-control',
            'placeholder':'Select a Topic'
            }))

    name=forms.CharField(label="Room Name",widget=forms.TextInput(attrs={
        "placeholder":"Room Name",
        "class":"col-12 form-control bg-dark border border-1 border-white mb-3 text-white",
        
    }))      

    description=forms.CharField(label="Room Description",widget=forms.Textarea(attrs={
        "placeholder":"Write a Description",
        "class":"col-12 form-control bg-dark border border-1 border-white mb-3 text-white"
    }))
    class Meta:
        model=Room
        fields="__all__"
        exclude=['host','participants']


class UserForm(forms.Form):
    username=forms.CharField(label="User Name",widget=forms.TextInput(attrs={
        "placeholder":"Enter User Name",
        "class":"col-12 form-control bg-dark border border-1 border-white mb-2 text-white",
        
    }))    
    password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={
        "placeholder":"Enter Password",
        "class":"col-12 form-control bg-dark border border-1 border-white mb-2 text-white",
    }))    
    password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={
        "placeholder":"Enter Confirm Password",
        "class":"col-12 form-control bg-dark border border-1 border-white mb-2 text-white",
    }))    
    
    userImage=forms.ImageField(label="User Image")
    