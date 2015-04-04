from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from mellonplanner.models import *

from django.core.context_processors import csrf

@login_required
def getschedules(request):
    profile = Profile.objects.get(user=request.user)
    context = {}
    context.update(csrf(request))
    errors = []
    context['errors'] = errors
    if not 'loc' in request.POST or not request.POST['loc']:
        errors.append('List of classes is required')
    if not 'minunits' in request.POST or not request.POST['minunits']:
        errors.append('Minimum units is required')
    if not 'maxunits' in request.POST or not request.POST['maxunits']:
        errors.append('Maximum units is required')
    if(request.POST['minunits'] < 0 or
       (request.POST['maxunits'] < request.POST['minunits'])):
        errors.append('Invalid units')
    list_of_classes = request.POST['loc'].split(", ")
    # Should check for validity of classes here
    # Then call the backend functions
    # and finally put pictures in the context dictionary
    return render(request, 'Hello.html', context)
    
@login_required
def home(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return render(request, 'Login_Page.html', {})
    context = {}
    context.update(csrf(request))
    return render(request, 'Hello.html', context)
    
def register(request):
    context = {}
    context.update(csrf(request))

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, 'Login_Page.html', context)

    errors = []
    context['errors'] = errors

    # Checks the validity of the form data
    if not 'username1' in request.POST or not request.POST['username1']:
	errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
	context['username'] = request.POST['username1']
    if not 'username2' in request.POST or not request.POST['username2']:
	errors.append('Confirm username is required.')
	
    if 'username1' in request.POST and 'username2' in request.POST \
       and request.POST['username1'] and request.POST['username2'] \
       and request.POST['username1'] != request.POST['username2']:
	errors.append('Usernames did not match.')

    if not 'password1' in request.POST or not request.POST['password1']:
	errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
	errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
       and request.POST['password1'] and request.POST['password2'] \
       and request.POST['password1'] != request.POST['password2']:
	errors.append('Passwords did not match.')

    if len(User.objects.filter(username = request.POST['username1'])) > 0:
	errors.append('There is already an account linked to that username')

    if errors:
        return render(request, 'Login_Page.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username1'], \
                                        password=request.POST['password1'])
    new_user.save()

    username = new_user.get_username()
    fname = ''
    lname = ''
    if 'fname' in request.POST and request.POST['fname']:
        fname = request.POST['fname']
    if 'lname' in request.POST and request.POST['lname']:
        lname = request.POST['lname']
    new_user_profile = Profile(user=new_user, first_name=fname, \
                               last_name=lname, username=username)
    new_user_profile.save()
    
    # Logs in the new user and redirects to his/her profile
    new_user = authenticate(username=request.POST['username1'], \
                            password=request.POST['password1'])
    login(request, new_user)
    return redirect('/myschedule/')
