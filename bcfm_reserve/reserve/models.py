from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile (models.Model):
	"""
	This class models the profile table in the database.
	----Fields----
	- user(foreign key) = links to User(UserID) with a foregin key
	- phone = a user's phone number
	----Methods----
	Author: Blaise Roberts
	"""

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = models.CharField(max_length=18)

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class ReservationType (models.Model):
	"""
	This class models the profile table in the database.
	----Fields----
	- label = string that represents the Type
	----Methods----
	Author: Blaise Roberts
	"""
	label = models.CharField(max_length=50)

	def __str__(self):
		return self.label

class VacancyStatus (models.Model):
	"""
	This class models the profile table in the database.
	----Fields----
	- label = string that represents the Status
	----Methods----
	Author: Blaise Roberts
	"""
	label = models.CharField(max_length=50)

	def __str__(self):
		return self.label

class SpaceType (models.Model):
	"""
	This class models the profile table in the database.
	----Fields----
	- label = string that represents the Type
	- monthly = boolean to show if a Type if for monthly or daily
	----Methods----
	Author: Blaise Roberts
	"""
	label = models.CharField(max_length=50)
	monthly = models.NullBooleanField()


	def __str__(self):
		return self.label

class ProductType (models.Model):
	"""
	This class models the profile table in the database.
	----Fields----
	- label = string that represents the Type
	----Methods----
	Author: Blaise Roberts
	"""
	label = models.CharField(max_length=50)


	def __str__(self):
		return self.label

class Parking (models.Model):
	"""
	This class models the profile table in the database.
	----Fields----
	- label = string that represents the Type
	----Methods----
	Author: Blaise Roberts
	"""
	label = models.CharField(max_length=50)

	def __str__(self):
		return self.label

class Building (models.Model):
	"""
	This class models the profile table in the database.
	----Fields----
	- title = string that is the title of the building
	- space_type(foreign key) = links to SpaceType with a foreign key
	- vacancy_status(foreign key) = links to VacancyStatus with a foreign key
	- space = string that is the space of the building
	- parking(foreign key) = links to Parking with a foreign key
	- weekly_access(Boolean) = true if buiding can be accessed during weekdays
	- price = int of the price per month
	- deposit = int of the price for deposit
	- contact_list(ManyToMany) = links to Users
	----Methods----
	Author: Blaise Roberts
	"""
	title = models.CharField(max_length=18)
	space_type = models.ForeignKey(SpaceType, 
        on_delete=models.CASCADE, related_name="buildings")
	vacancy_status = models.ForeignKey(VacancyStatus, 
        on_delete=models.CASCADE, related_name="buildings")
	space = models.CharField(max_length=18)
	parking = models.ForeignKey(Parking, 
        on_delete=models.CASCADE, related_name="buildings")
	weekly_access = models.BooleanField()
	price = models.IntegerField()
	deposit = models.IntegerField()
	contact_list = models.ManyToManyField(User, related_name='building_requests', blank=True)


	def __str__(self):
		return self.title

class Space (models.Model):
	"""
	This class models the profile table in the database.
	----Fields----
	- title = name of space
	- space_type(foreign key) = links to SpaceType with a foregin key
	- tables = # of tables
	- space(string) = ammount of space ('10x10')
	- parking(string) = description of parking ('parking for 1 vehicle')
	- price = int of the price per day
	- likes(ManytoMany): stores User Instances
    - dislikes(ManytoMany): stores User Instances
	----Methods----
	Author: Blaise Roberts
	"""
	title = models.CharField(max_length=18)
	space_type = models.ForeignKey(SpaceType, 
        on_delete=models.CASCADE, related_name="spaces")
	tables = models.IntegerField()
	space = models.CharField(max_length=10)
	parking = models.ForeignKey(Parking, 
        on_delete=models.CASCADE, related_name="spaces")
	price = models.IntegerField(default=10)
	likes = models.ManyToManyField(User, related_name='likes', blank=True)
	dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)

	def __str__(self):
		return self.title

class Reservation (models.Model):
	"""
	This class models the reservation table in the database
	----Fields----
	- customer(foreign key) = links to User with a foregin key
	- space = string that is the space of the building
	- reservation_date = date in the format 'YYYY-MM-DD'
	- creation_date = date in the format 'YYYY-MM-DD'
	- paid_date = date in the format 'YYYY-MM-DD'
	- reservation_type(foreign key) = links to ReservationType with a foregin key
	- hold_name = string that is the hold name for an in person transaction. (nullable)
	- product_types(ManytoMany): stores ProductType Instances

	----Methods----
	Author: Blaise Roberts
	"""
	customer = models.ForeignKey(User, 
        on_delete=models.CASCADE, related_name="reservations")
	space = models.ForeignKey(Space, 
        on_delete=models.CASCADE, related_name="reservations")
	reservation_date = models.DateField()
	creation_date = models.DateField()
	paid_date = models.DateField(blank=True, null=True)
	reservation_type = models.ForeignKey(ReservationType, related_name='reservations')
	hold_name = models.CharField(max_length=30, blank=True, null=True)
	product_types = models.ManyToManyField(ProductType, related_name='reservations', blank=True)

	def __str__(self):
		return "{} {} by {} {}".format(self.space, self.reservation_type, self.customer.first_name, self.customer.last_name, self.reservation_date)
