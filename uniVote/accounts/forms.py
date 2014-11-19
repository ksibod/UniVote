from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


# This is the form used to register a user:
class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        # These are the fields the user needs to enter to make a account:
        fields = {'first_name': forms.TextInput(attrs={'class': 'formInput'}),
                  'last_name': forms.TextInput(attrs={'class': 'formInput'}),
                  'email': forms.TextInput(attrs={'class': 'formInput'}),
                  'username': forms.TextInput(attrs={'class': 'formInput'}),
                  'password1': forms.TextInput(attrs={'class': 'formInput'}),
                  'password2': forms.TextInput(attrs={'class': 'formInput'})}