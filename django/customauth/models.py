from django.db import models

from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django import forms

import hashlib
import random

from api.models import Token

class UserManager(BaseUserManager):

	def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
		now = timezone.now()
		if not email:
		  raise ValueError(_('The given email must be set'))
		email = self.normalize_email(email)
		
		user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		
		user.add_token()
		
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
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	
	objects = UserManager()
 
	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		self.first_name

	def add_token(self):
		# assign a token to the user
		t = Token(user=self,daily_computation_time=600)
		t.token = t.generate_token(self.email)
		t.save()