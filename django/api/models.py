from django.db import models

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


import hashlib
import random

class Token(models.Model):
	"""
	defining api access and use
	"""
	
	user = models.ForeignKey('customauth.User', on_delete=models.CASCADE)
	
	token = models.CharField(_('token'), max_length=200, blank=True, null=True)
	daily_computation_time = models.IntegerField(_('daily computation time'), default=0)
	used_computation_time = models.IntegerField(_('used computation time'), default=0)
	last_api_call = models.DateTimeField(_('last api call'), default=timezone.now)
	
	def generate_token(self,data):
		return hashlib.sha1( (str(random.random()) + data + str(random.random())).encode('utf-8') ).hexdigest()
		
	def check_reset_used_computation_time(self):
		if self.last_api_call < timezone.now().replace(hour=0, minute=0, second=0, microsecond=0):
			self.used_computation_time = 0
			self.last_api_call = timezone.now()
			self.save()