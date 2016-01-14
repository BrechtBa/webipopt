from django.db import models

from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django import forms

import hashlib
import random

class UserManager(BaseUserManager):

	def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
		now = timezone.now()
		if not email:
		  raise ValueError(_('The given email must be set'))
		email = self.normalize_email(email)
		
		user = self.model(email=email, token=token, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, daily_computation_time=600, **extra_fields)
		user.set_password(password)
		
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		return self._create_user( email, password, False, False, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		user = self._create_user(email, password, True, True, **extra_fields)
		user.is_active=True
		user.save(using=self._db)
		return user

		
class User(AbstractBaseUser, PermissionsMixin):

	email = models.EmailField(_('email address'), max_length=255, unique=True)
	first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
	last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)

	is_staff = models.BooleanField(_('staff status'), default=False,help_text=_('Designates whether the user can log into this admin site.'))
	is_active = models.BooleanField(_('active'), default=False,help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	
	token = models.CharField(_('token'), max_length=200, blank=True, null=True)
	daily_computation_time = models.IntegerField(_('daily computation time'), default=0)
	used_computation_time = models.IntegerField(_('used computation time'), default=0)
	last_api_call = models.DateTimeField(_('last api call'), default=timezone.now)
	
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	
	objects = UserManager()
 
	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		self.first_name

	def generate_token(self):
		# generate a token
		self.token = hashlib.sha1( (str(random.random()) + self.email + str(random.random())).encode('utf-8') ).hexdigest()
	
	def initialize_api_properties(self):
		self.generate_token()
		self.daily_computation_time = 600