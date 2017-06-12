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
	phone = models.CharField(max_length=18, blank=True, null=True)

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
	label = models.CharField(max_length=18)

	def __str__(self):
		return self.label

class SpaceType (models.Model):
	"""
	This class models the profile table in the database.
	----Fields----
	- label = string that represents the Type
	----Methods----
	Author: Blaise Roberts
	"""
	label = models.CharField(max_length=18)

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
	- vacancy_status(foreign key) = links to VacancyStatus with a foregin key
	- description = string that is the description of the building
	- contact_list(ManyToMany) = links to Users
	- open_access(Boolean) = true if buiding can be accessed during weekdays
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
	contact_list = models.ManyToManyField(User, related_name='building_requests')


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
	price = models.IntegerField
	likes = models.ManyToManyField(User, related_name='likes')
	dislikes = models.ManyToManyField(User, related_name='dislikes')

	def __str__(self):
		return self.title

class Reservation (models.Model):
	"""
	This class models the reservation table in the database
	----Fields----
	----Methods----
	Author: Blaise Roberts
	"""
	customer = models.ForeignKey(User, 
        on_delete=models.CASCADE, related_name="reservations")
	space = models.ForeignKey(Space, 
        on_delete=models.CASCADE, related_name="reservations")
	date = models.DateField()
	status = models.ForeignKey(VacancyStatus, 
        on_delete=models.CASCADE, related_name="reservations")
	reservation_types = models.ManyToManyField(ReservationType, related_name='reservations')

	def __str__(self):
		return "Reservation for {} by {} {} on {}".format(self.space.title, self.customer.first_name, self.customer.last_name, self.date)
