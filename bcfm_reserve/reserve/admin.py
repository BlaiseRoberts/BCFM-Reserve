from django.contrib import admin
from .models import Reservation, Space, Building, SpaceType,\
ReservationType, VacancyStatus, Parking, Profile

@admin.register(Reservation, Space, Building, SpaceType,
ReservationType, VacancyStatus, Parking, Profile)
class Admin(admin.ModelAdmin):
    pass

