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
				space.status = 'Open'

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








