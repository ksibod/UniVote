from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.core.context_processors import csrf
from django.contrib.auth.models import User

#Import a user registration form
from forms import UserRegisterForm

#import json stuff
import json

#import mail stuff
from django.core.mail import EmailMessage


# User authentication in Django
# https://docs.djangoproject.com/en/dev/topics/auth/


# User Login View
def user_login(request):
    if request.user.is_anonymous():
        if request.method == 'POST':
            # NEED A FORM FOR USER TO LOGIN:

            username = request.POST['username']
            password = request.POST['password']

            #This authenticates the user
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # This logs him in:
                    login(request, user)
                    return HttpResponse("loginSuccess")
                else:
                    # Return a 'disabled account' message:
                    return HttpResponse("loginFail")

            else:
                # User not in the system
                return HttpResponse("loginFail")
        else:
            return render(request, 'accounts/login.html')
    else:
        return HttpResponseRedirect("/elections")


# User Logout View
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


# User Register View
def user_register(request):
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("registerSuccess")
            else:
                print form.error_messages
                return HttpResponse(form.error_messages)
        else:
            form = UserRegisterForm()
        context = {}
        context.update(csrf(request))
        context['form'] = form
        #Pass the context to a template
        return render(request, 'accounts/register.html', context)
    else:
        return HttpResponseRedirect('/')


# User forgot password
def user_forgot_password(request):
    if request.method == 'POST':
        emailAddress = request.POST['email']
        message = "<html><p>You have requested this email to update your password for the uniVote application.</p><p>Please click the link below to continue:</p><a href='127.0.0.1:8000'>Update Password</a><p>If you have received this email in error, please disregard.</p><p>Thanks,</p><p>uniVote! Team</p></html>"
        email = EmailMessage("Password Reset", message, to=[emailAddress])
        #email.attach_file("static/images/uniVote.png")
        email.content_subtype = "html"
        email.send()
        return HttpResponse("forgotPassSuccess")
