from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,\
	HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.admin.views.decorators import staff_member_required



from reserve.forms import UserForm, LoginForm, ProfileForm, EditUserForm,\
	ReservationForm
from reserve.models import Reservation, Space, Building, SpaceType,\
	ReservationType, VacancyStatus, Parking, Profile
from django.contrib.auth.models import User

import datetime
import pytz

@staff_member_required
def admin_space_details(request, space_id, date):
	if request.method == 'POST':
		reservation_form = ReservationForm(request.POST)
		space = Space.objects.get(pk=space_id)

		cancel_confirm_button = request.POST.get("cancel_confirm_button", "")
		pay_reserve_button = request.POST.get("pay_reserve_button", "")

		if cancel_confirm_button == "Cancel":
			reservation_type = ReservationType.objects.get(pk=2)
			r = space.reservations.filter(date=date).latest('pk')
			r.reservation_type = reservation_type
			r.save()
			return HttpResponseRedirect(reverse('reserve:admin_space', 
	                args=[r.space.id, date]))

		if cancel_confirm_button == "Confirm":
			reservation_type = ReservationType.objects.get(pk=4)
			r = space.reservations.filter(date=date).latest('pk')
			r.reservation_type = reservation_type
			r.save()
			return HttpResponseRedirect(reverse('reserve:admin_space', 
	                args=[r.space.id, date]))
		if pay_reserve_button == "Pay":
			reservation_type = ReservationType.objects.get(pk=3)
		if pay_reserve_button == "Reserve":
			reservation_type = ReservationType.objects.get(pk=1)
		try:
			if reservation_form.is_valid():
				r = Reservation.objects.get(space_id=space_id, date=date, customer=request.user)
				r.reservation_type = reservation_type
				r.hold_name = reservation_form.cleaned_data['hold_name']
				r.save()
				return HttpResponseRedirect(reverse('reserve:admin_space', 
		                args=[r.space.id, date]))
		except:
			if reservation_form.is_valid():
				r = Reservation(
					customer = request.user 
				)
				r.hold_name = reservation_form.cleaned_data['hold_name']
				r.space = space
				r.date = date
				r.reservation_type = reservation_type
				r.save()
				return HttpResponseRedirect(reverse('reserve:admin_space', 
		                args=[r.space.id, date]))
		
		
	elif request.method == 'GET':
		try:
			reservation_form = ReservationForm()
			space = Space.objects.get(pk=space_id)
			reservations = space.reservations.filter(date=date, reservation_type_id__in=[1,3,4]).order_by('-pk')
			if reservations:
				status = reservations[0]
				space.status = status
			else:
				space.status = {'reservation_type':'Open'}

			template_name = 'space_detail.html'

			return render(request, template_name, {'space':space, 'date':date,
				'reservation_form':reservation_form})
		except:
			error = "Space does not Exist"
			error_details = "You're searching for a space that doesn't exist."
			template_name = 'error.html'

			return render(request, template_name, {'error':error, 
				'error_details':error_details})

@staff_member_required
def admin_building_details(request, building_id):
	try:
		building = Building.objects.get(pk=building_id)
		template_name = 'building_detail.html'
		contact_list = building.contact_list.all()
		return render(request, template_name, {'building':building,
				'contact_list':contact_list})
	except:
		error = "Building does not Exist"
		error_details = "You're trying to view a building that doesn't\
			exist."
		template_name = 'error.html'

		return render(request, template_name, {'error':error, 
			'error_details':error_details})

@staff_member_required
def remove_contact(request, building_id, user_id):
	try:
		building = Building.objects.get(pk=building_id)
		customer = User.objects.get(pk=user_id)
		building.contact_list.remove(customer)
		template_name = 'building_detail.html'
		contact_list = building.contact_list.all()
		return render(request, template_name, {'building':building,
				'contact_list':contact_list})
	except:
		error = "Building or User does not Exist"
		error_details = "You're trying to view a building or user that doesn't\
			exist."
		template_name = 'error.html'

		return render(request, template_name, {'error':error, 
			'error_details':error_details})

@staff_member_required
def admin_reservation(request):
	if request.method == 'GET':
		users = User.objects.filter(is_staff=True)
		reservations= []
		for user in users:
			user_reservations = Reservation.objects.filter(customer=user).order_by('-date')[:20]
			for reservation in user_reservations:
				reservations.append(reservation)
		template_name = 'staff.html'
		return render(request, template_name, {'reservations':reservations})

@staff_member_required
def user_permissions(request):
	if request.method == 'POST':
		admin_button = request.POST.get("admin_button", "")
		if admin_button == "Make Admin":
			user_id = request.POST['user_select']
			user = User.objects.get(pk=user_id)
			user.is_staff = True
			user.is_admin = True
			user.save()
		if admin_button == "Remove Admin":
			user_id = request.POST['user_select']
			user = User.objects.get(pk=user_id)
			user.is_staff = False
			user.is_admin = False
			user.save()
		users = User.objects.all()
		template_name = 'make_admin.html'
		return render(request, template_name, {'users':users})

	if request.method == 'GET':
		users = User.objects.all()
		template_name = 'make_admin.html'
		return render(request, template_name, {'users':users})

@staff_member_required
def reporting(request, date=None):
	form_data = request.GET
	date_today = datetime.datetime.now(pytz.timezone('US/Pacific'))
	if date:
		pass
	else:
		if form_data:
				date = form_data['date_picker']
				if date == "":
					date_today = datetime.datetime.now(pytz.timezone('US/Pacific'))
					date_ordinal = date_today.isoweekday()
					days_ahead = 6 - date_ordinal
					if days_ahead == -1:
						days_ahead += 7
					next_date = date_today+datetime.timedelta(days=days_ahead)
					date = str(next_date)[:10]
	all_spaces = Space.objects.all()
	open_space_count = 0
	occupied_count = 0
	reserved_count = 0
	cancelled_count = 0
	paid_count = 0
	confirmed_count = 0
	for space in all_spaces:
		reservations = space.reservations.filter(date=date, reservation_type_id__in=[1,2,3,4])
		if reservations:
			occupied_count += 1
			if reservations[0].reservation_type.pk == 1:
				reserved_count +=1
			if reservations[0].reservation_type.pk == 2:
				cancelled_count +=1
				open_space_count += 1
			if reservations[0].reservation_type.pk == 3:
				paid_count +=1
			if reservations[0].reservation_type.pk == 4:
				confirmed_count +=1	
		else:
			open_space_count += 1

	template_name = 'reporting.html'

	return render(request, template_name, {'occupied_count':occupied_count,
		'open_space_count':open_space_count,'date':date, 
		'reserved_count':reserved_count, 'cancelled_count':cancelled_count,
		'paid_count':paid_count, 'confirmed_count':confirmed_count})



