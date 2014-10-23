from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# This is the form used to register a user:
class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        # These are the fields the user needs to enter to make a account:
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password1', 'password2')


# class AuthenticationForm(AuthenticationForm):

#     class Meta:
#         model = User
#         fields = ('username', 'password')
