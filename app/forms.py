from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'image', 'bio', 'phone']
        widgets = {
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Phone Number',
                    'value': '{{profile.phone}}',
                    'data-mask': '(+000) 00-000-000'

                }
            )
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 17:
            raise forms.ValidationError('Denied! Phone Field is not complete')
        else:
            return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        for obj in Profile.objects.all():
            if obj.email == email:
                raise forms.ValidationError('Email already exists')
            else:
                return email
