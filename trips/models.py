from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid 

from django.shortcuts import reverse


# Create your models here. 
class User(AbstractUser):
	pass


class Trip(models.Model):
	REQUESTED = 'REQUESTED'
	STARTED = 'STARTED'
	IN_PROGRESS = 'IN_PROGRESS'
	COMPLETED = 'COMPLETED'
	STATUSES = (
		(REQUESTED, REQUESTED),
		(STARTED, STARTED),
		(IN_PROGRESS, IN_PROGRESS),
		(COMPLETED, COMPLETED),
	)

	id = models.UUIDField(primary_key= True, default = uuid.uuid4, editable = False)
	created = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
	pick_up_address = models.CharField(max_length = 255)
	drop_off_address = models.CharField(max_length = 255)
	status = models.CharField(
		max_length = 20, choices = STATUSES, default = REQUESTED)
	driver = models.ForeignKey(settings.AUTH_USER_MODEL,
		null = True,
		blank = True,
		on_delete = models.DO_NOTHING,
		related_name = 'trips_as_driver',
		)
	rider = models.ForeignKey(settings.AUTH_USER_MODEL,
		null = True,
		blank = True,
		on_delete = models.DO_NOTHING,
		related_name = 'trips_as_rider',
		)

	def __str__(self):
		return f'{self.id}'

	def get_absolute_url(self):
		return reverse('trip:trip_detail', kwargs = {'trip_id': self.id})

