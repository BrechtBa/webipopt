from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	# Links UserProfile to a User model instance.
	user = models.OneToOneField(User)

	# The additional attributes
	token = models.CharField(max_length=200)
	
	def __str__(self):
		return self.user.username