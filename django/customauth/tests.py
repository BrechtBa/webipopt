from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from .models import User
from .forms import UserCreationForm

class RegistrationTest(TestCase):

	def test_registration_form_correct(self):
		"""
		tests a correct registration form
		"""
		
		data = {'email': 'a@b.com','password1':'azertyuiop','password2':'azertyuiop'}
		form = UserCreationForm(data=data)
		self.assertTrue( form.is_valid() )
		
		user = form.save()
		
		self.assertTrue( len(user.token)>20 )
		self.assertTrue( user.daily_computation_time == 600 )
		self.assertTrue( user.used_computation_time == 0 )
		
	def test_registration_form_email(self):
		"""
		tests a registration form with an invalid email adress
		"""
		
		data = {'email': 'ab.com','password1':'azertyuiop','password2':'azertyuiop'}
		form = UserCreationForm(data=data)
		self.assertFalse( form.is_valid() )	
		
	def test_registration_form_password(self):
		"""
		tests a registration form with unequal passwords
		"""
		
		data = {'email': 'a#b.com','password1':'azertyuiop','password2':'azertguiop'}
		form = UserCreationForm(data=data)
		self.assertFalse( form.is_valid() )	
	