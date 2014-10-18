from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password1', 'password2')


# class AuthenticationForm(AuthenticationForm):

#     class Meta:
#         model = User
#         fields = ('username', 'password')
