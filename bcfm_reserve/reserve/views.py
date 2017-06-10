from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from reserve.forms import UserForm, LoginForm, ProfileForm
from .models import Reservation, Space, Building, SpaceType,\
ReservationType, VacancyStatus, Parking, Profile


def index(request):
	if request.method == 'POST':
		pass
	elif request.method == 'GET':
		template_name = 'index.html'

		return render(request, template_name, {})

def browse(request):
	if request.method == 'POST':
		pass
	elif request.method == 'GET':
		template_name = 'browse.html'

		return render(request, template_name, {})

def account(request, user_id):
	if request.method == 'POST':
		pass
	elif request.method == 'GET':
		profile = Profile.objects.get(user_id=user_id)
		template_name = 'account.html'

		return render(request, template_name, {'profile':profile})

def reservation(request, user_id):
	if request.method == 'POST':
		pass
	elif request.method == 'GET':
		template_name = 'reservation.html'

		return render(request, template_name, {})


def register(request):
    """
    Handles the creation of a new user for authentication
    ---Arguments---
    None
    ---GET---
    Renders register.html
        ---Context---
        'user_form': the form from user_form.py
    ---POST---
    runs the login_user function
    Author: Blaise Roberts
    """

    # A boolean value for telling the template 
    # whether the registration was successful.
    # Set to False initially. Code changes value to True when registration 
    # succeeds.
    registered = False

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            profile = Profile.objects.get(user=user)
            profile.phone = profile_form.cleaned_data['phone']
            profile.save()
            # Update our variable to tell the template 
            # registration was successful.
            registered = True

        return login_user(request)

    elif request.method == 'GET':
        user_form = UserForm()
        profile_form = ProfileForm()
        template_name = 'register.html'
        return render(request, template_name, {'user_form': user_form,
        	"profile_form":profile_form})

def login_user(request):
    '''Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    Author: Beve Strownlee
    '''

    # Obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        
        # Use the built-in authenticate method to verify
        username=request.POST['username']
        password=request.POST['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            return HttpResponseRedirect('/')

        else:
            # Bad login details were provided. So we can't log the user in.
            return HttpResponse("Invalid login details supplied.")


        return render(request, 'login.html', {}, context)
    elif request.method == 'GET':
        login_form = LoginForm()
        
        template_name = "login.html"
        return render(request, template_name, {"login_form":login_form})

@login_required
def logout_user(request):
	"""
	This method is invoked to logout the user and redirect them to the index
	 ---Arguments---
    None
	Author: Blaise Roberts
	"""

    # Since we know the user is logged in, we can now just log them out.
	logout(request)

    # Take the user back to the homepage. 
	return HttpResponseRedirect(reverse('reserve:index'))




