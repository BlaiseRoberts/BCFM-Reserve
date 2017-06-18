from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,\
	HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from reserve.forms import UserForm, LoginForm, ProfileForm, EditUserForm
from reserve.models import Reservation, Space, Building, SpaceType,\
	ReservationType, VacancyStatus, Parking, Profile

import datetime
import pytz

def index(request):
	try:
		liked_spaces = request.user.likes.all()
		print(liked_spaces)
	except:
		liked_spaces = []
		print("Anon User")

	recommended_spaces = []
	space_types = set()
	date_today = datetime.datetime.now(pytz.timezone('US/Pacific'))
	date_ordinal = date_today.isoweekday()
	days_ahead = 6 - date_ordinal
	if days_ahead <= 0:
		days_ahead += 7
	next_date = date_today+datetime.timedelta(days=days_ahead)

	for space in liked_spaces:
		print(space.reservations.filter(date=str(next_date)[:10],reservation_type__in=[1,3,4]).count())
		if space.reservations.filter(date=str(next_date)[:10],reservation_type__in=[1,3,4]).count() == 0:
			recommended_spaces.append(space)
			space_types.add(space.space_type)

	template_name = 'index.html'

	return render(request, template_name, {'spaces':recommended_spaces,
		'next_date':str(next_date)[:10], 'space_types':space_types})

def rules(request):
	template_name = 'rules.html'

	return render(request, template_name, {})

def buildings(request):
	if request.method == 'POST':
		buildings = Building.objects.filter(weekly_access=True)
		for building in buildings:
			building.contact_list.add(request.user)
		return HttpResponseRedirect(reverse('reserve:buildings'))

	if request.method == 'GET':
		buildings = Building.objects.all()
		building_types = SpaceType.objects.filter(monthly=True)
		template_name = 'buildings.html'

		return render(request, template_name, {'buildings':buildings, 
			'building_types':building_types})

def building_details(request, building_id):
	if request.method == 'POST':
		building = Building.objects.get(pk=building_id)
		building.contact_list.add(request.user)

		return HttpResponseRedirect(reverse('reserve:building_details', 
		                args=[building.id]))

	if request.method == 'GET':
		try:
			building = Building.objects.get(pk=building_id)
			template_name = 'building_detail.html'
			contact_list = building.contact_list.all()
			if request.user in contact_list:
				on_list = True
				return render(request, template_name, {'building':building,
					'on_list':on_list})
			else:
				return render(request, template_name, {'building':building})
		except:
			error = "Building does not Exist"
			error_details = "You're trying to view a building that doesn't\
				exist."
			template_name = 'error.html'

			return render(request, template_name, {'error':error, 
				'error_details':error_details})

def browse(request, date=None):
	if request.method == 'GET':
		form_data = request.GET
		all_spaces = Space.objects.all()
		space_types = SpaceType.objects.filter(monthly=0)
		spaces = []
		if date:
			if request.user.is_staff:
				pass
			else:
				date_time = datetime.datetime.strptime(date, '%Y-%m-%d')
				if date > str(datetime.date.today()+datetime.timedelta(days=21\
						)) or date_time.isoweekday() in range(1, 6)\
						or date <= str(datetime.date.today()):
					error = "Outside Date Range"
					error_details = "You can not reserve spaces on a weekday\
						and you can not reserve spaces more than 3 weeks ahead or\
						you may have selected a past date."
					template_name = 'error.html'

					return render(request, template_name, {'error':error, 
						'error_details':error_details})
				pass
		else:
			if form_data:
				date = form_data['date_picker']
				if date == "":
					date_today = datetime.datetime.now(pytz.timezone('US/Pacific'))
					date_ordinal = date_today.isoweekday()
					days_ahead = 6 - date_ordinal
					if days_ahead <= 0:
						days_ahead += 7
					next_date = date_today+datetime.timedelta(days=days_ahead)
					date = str(next_date)[:10]
				if request.user.is_staff:
					pass
				else:
					date_time = datetime.datetime.strptime(date, '%Y-%m-%d')
					if date > str(datetime.date.today()+datetime.timedelta(days=21\
						)) or date_time.isoweekday() in range(1, 6)\
						or date <= str(datetime.datetime.now(pytz.timezone('US/Pacific'))):
						error = "Outside Date Range"
						error_details = "You can not reserve spaces on a weekday\
							and you can not reserve spaces more than 3 weeks ahead\
							or you may have selected a past date."
						template_name = 'error.html'

						return render(request, template_name, {'error':error, 
							'error_details':error_details})
		for space in all_spaces:
			reservations = space.reservations.filter(date=date, reservation_type_id__in=[1,3,4])
			if reservations:
				status = reservations[0]
				space.status = status
			else:
				space.status = 'Open'
			spaces.append(space)

		template_name = 'browse.html'

		return render(request, template_name, {'spaces':spaces, 'date':date,
			'space_types':space_types})

def space_details(request, space_id, date):
	if request.method == 'POST':
		space = Space.objects.get(pk=space_id)

		like_dislike_button = request.POST.get("like_dislike_button", "")

		if like_dislike_button == "Like":
			space.dislikes.clear()
			space.likes.add(request.user)
			return HttpResponseRedirect(reverse('reserve:space', 
	                args=[space.id, date]))

		if like_dislike_button == "Dislike":
			space.likes.clear()
			space.dislikes.add(request.user)
			return HttpResponseRedirect(reverse('reserve:space', 
	                args=[space.id, date]))

		reservation_type = ReservationType.objects.get(pk=1)
		total_reservations = Reservation.objects.filter(customer=request.user, date=date).count()
		if total_reservations < 6:
			try:
				r = Reservation.objects.get(space_id=space_id, date=date, customer=request.user)
				r.reservation_type = reservation_type
				r.save()
				space.dislikes.clear()
				space.likes.add(request.user)
				return HttpResponseRedirect(reverse('reserve:space', 
		                args=[r.space.id, date]))
			except:
				r = Reservation(
					customer = request.user
				)
				r.space = space
				r.date = date
				r.reservation_type = reservation_type
				r.save()
				space.dislikes.clear()
				space.likes.add(request.user)
				return HttpResponseRedirect(reverse('reserve:space', 
		                args=[r.space.id, date]))
		else:
			error = "Too Many Reservations"
			error_details = "You can cancel a different reservation on this\
				date or you can call 254-939-6411 and speak to the office\
				if you need to reserve more than 6 spaces a day."
			template_name = 'error.html'

			return render(request, template_name, {'error':error, 
				'error_details':error_details})

	elif request.method == 'GET':
		try:
			space = Space.objects.get(pk=space_id)
			reservations = space.reservations.filter(date=date, reservation_type_id=1)
			if reservations:
				status = reservations[0]
				space.status = status
			else:
				space.status = 'Open'
			user_liked = False
			user_disliked = False
			likes_list = space.likes.all()
			dislikes_list = space.dislikes.all()
			if request.user in likes_list:
				user_liked = True
			if request.user in dislikes_list:
				user_disliked = True

			template_name = 'space_detail.html'

			return render(request, template_name, {'space':space, 'date':date,
				'user_liked':user_liked, 'user_disliked':user_disliked})
		except:
			error = "Space does not Exist"
			error_details = "You're searching for a space that doesn't exist."
			template_name = 'error.html'

			return render(request, template_name, {'error':error, 
				'error_details':error_details})

def account(request, user_id):
	if str(request.user.id) == user_id:
		profile = Profile.objects.get(user_id=user_id)
		template_name = 'account.html'
		return render(request, template_name, {'profile':profile})
	else:
		error = "No Access"
		error_details = "You cannot edit another user's account, nice try."
		template_name = 'error.html'

		return render(request, template_name, {'error':error, 
			'error_details':error_details})

def edit_account(request, user_id):
	if request.method == 'POST':
		user_form = EditUserForm(request.POST)
		profile_form = ProfileForm(request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			updated_user = request.user
			updated_user.first_name = user_form.cleaned_data['first_name']
			updated_user.last_name = user_form.cleaned_data['last_name']
			updated_user.email = user_form.cleaned_data['email']
			updated_user.save()

			updated_account = Profile.objects.get(user=request.user)
			updated_account.phone = profile_form.cleaned_data['phone']
			updated_account.save()

			return HttpResponseRedirect(reverse('reserve:my_account',
			    args=[request.user.id]))
		else:
			return HttpResponseRedirect(reverse('reserve:my_account',
			    args=[request.user.id]))

	elif request.method == 'GET':
		if str(request.user.id) == user_id:
			profile = Profile.objects.get(user_id=user_id)
			user_form = EditUserForm(instance=profile.user)
			profile_form = ProfileForm(instance=profile)
			template_name = 'edit_account.html'
			return render(request, template_name, {'user_form':user_form,'profile_form':profile_form})
		else:
			error = "No Access"
			error_details = "You cannot edit another user's account, nice try."
			template_name = 'error.html'

			return render(request, template_name, {'error':error, 
				'error_details':error_details})

def reservation(request, user_id):
	if request.method == 'POST':
		pass
	elif request.method == 'GET':
		reservations = Reservation.objects.filter(customer_id=user_id).order_by('-date')[:12]
		template_name = 'reservation.html'
		return render(request, template_name, {'reservations':reservations})

def delete_reservation(request, reservation_id, date):
	r = Reservation.objects.get(pk=reservation_id, date=date)
	reservation_type = ReservationType.objects.get(pk=2)
	if request.user == r.customer:
		r.reservation_type = reservation_type
		r.save()
		return HttpResponseRedirect(reverse('reserve:reservation', 
            args=[request.user.id]))
	else:
		error = "No Access"
		error_details = "You cannot edit another user's reservations,\
			nice try."
		template_name = 'error.html'

		return render(request, template_name, {'error':error, 
			'error_details':error_details})


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




