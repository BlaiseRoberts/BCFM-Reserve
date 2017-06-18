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

def admin_space_details(request, space_id, date):
	if request.method == 'POST':
		space = Space.objects.get(pk=space_id)

		cancel_confirm_button = request.POST.get("cancel_confirm_button", "")

		if cancel_confirm_button == "Cancel":
			reservation_type = ReservationType.objects.get(pk=2)
			r = space.reservations.latest('pk')
			r.reservation_type = reservation_type
			r.save()
			return HttpResponseRedirect(reverse('reserve:admin_space', 
	                args=[r.space.id, date]))

		if cancel_confirm_button == "Confirm":
			reservation_type = ReservationType.objects.get(pk=4)
			r = space.reservations.latest('pk')
			r.reservation_type = reservation_type
			r.save()
			return HttpResponseRedirect(reverse('reserve:admin_space', 
	                args=[r.space.id, date]))

		reservation_type = ReservationType.objects.get(pk=3)
		try:
			r = Reservation.objects.get(space_id=space_id, date=date, customer=request.user)
			r.reservation_type = reservation_type
			r.save()
			return HttpResponseRedirect(reverse('reserve:admin_space', 
	                args=[r.space.id, date]))
		except:
			r = Reservation(
				customer = request.user
			)
			r.space = space
			r.date = date
			r.reservation_type = reservation_type
			r.save()
			return HttpResponseRedirect(reverse('reserve:admin_space', 
	                args=[r.space.id, date]))
		
	elif request.method == 'GET':
		try:
			space = Space.objects.get(pk=space_id)
			reservations = space.reservations.filter(date=date, reservation_type_id__in=[1,3,4]).order_by('-pk')
			if reservations:
				status = reservations[0]
				space.status = status
			else:
				space.status = 'Open'

			template_name = 'space_detail.html'

			return render(request, template_name, {'space':space, 'date':date})
		except:
			error = "Space does not Exist"
			error_details = "You're searching for a space that doesn't exist."
			template_name = 'error.html'

			return render(request, template_name, {'error':error, 
				'error_details':error_details})