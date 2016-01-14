from django.views.generic import TemplateView, CreateView, FormView, RedirectView

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy

class Index(TemplateView):
    template_name = 'webinterface/index.html'
	
class RegisterView(CreateView):
	form_class = UserCreationForm
	model = User
	template_name = 'webinterface/register.html'
	url = reverse_lazy('webinterface:index')
	
class LoginView(FormView):
	form_class = AuthenticationForm
	template_name = 'webinterface/login.html'
	
	success_url = reverse_lazy('webinterface:index')
	
	def form_valid(self, form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
	
		if user is not None and user.is_active:
			login(self.request, user)
			return super(LoginView, self).form_valid(form)
		else:
			return self.form_invalid(form)
			
class LogoutView(RedirectView):
	url = reverse_lazy('webinterface:index')

	def get(self, request, *args, **kwargs):
		logout(request)
		return super(LogoutView, self).get(request, *args, **kwargs)
		
