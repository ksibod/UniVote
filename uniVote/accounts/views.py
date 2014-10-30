from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response, render
from django.core.context_processors import csrf

#Import a user registration form
from accounts.forms import UserRegisterForm

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
                    # redirect to elections:
                    return HttpResponseRedirect('/elections/')
                else:
                    # Return a 'disabled account' message:
                    return HttpResponse("Not active")

            else:
                return HttpResponse("Wrong username/password")
    else:
        return HttpResponseRedirect("/elections")
    return HttpResponseRedirect("/")


# User Logout View
def user_logout(request):
    logout(request)
    # return HttpResponse('YOU HAVE BEEN LOGGED OUT.')
    return render(request, 'accounts/logout.html')


# User Register View
def user_register(request):
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid:
                form.save()
                return render(request, 'accounts/registered.html')
                #return HttpResponse('User created succcessfully.')
        else:
            form = UserRegisterForm()
        context = {}
        context.update(csrf(request))
        context['form'] = form
        #Pass the context to a template
        return render(request, 'accounts/register.html', context)
        # return render_to_response('accounts/register.html', context)
    else:
        return HttpResponseRedirect('/')
