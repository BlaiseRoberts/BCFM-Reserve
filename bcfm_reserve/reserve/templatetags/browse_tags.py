from reserve.models import Space, Reservation, Building

from django import template

register = template.Library()

@register.simple_tag
def get_open_count(date, space_type_id):
	spaces = Space.objects.filter(space_type_id=space_type_id)
	reservations = []
	for space in spaces:
		try:
			reservations.append(Reservation.objects.get(space=space, date=date, reservation_type_id=1))
		except:
			pass
	reservation_count = len(reservations)
	if date == "":
		reservation_count = spaces.count()
	return spaces.count() - reservation_count

@register.simple_tag
def get_building_count(space_type_id):
	building_count = Building.objects.filter(space_type_id=space_type_id, vacancy_status_id=1).count()
	return building_count