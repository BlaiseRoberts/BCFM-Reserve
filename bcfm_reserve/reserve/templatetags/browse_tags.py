from reserve.models import Space, Reservation

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