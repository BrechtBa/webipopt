from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, FormView, RedirectView
from django.shortcuts import render

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy

from customauth.models import User
from customauth.forms import UserCreationForm
from api.models import Token

from urllib.parse import urlencode
from urllib.request import Request, urlopen

class Index(TemplateView):
    template_name = 'webinterface/index.html'
	
class RegisterView(CreateView):
	form_class = UserCreationForm
	model = User
	template_name = 'webinterface/register.html'
	success_url = reverse_lazy('webinterface:dashboard')
	
	def form_valid(self, form):
		valid = super(RegisterView, self).form_valid(form)
		email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
		user = authenticate(email=email, password=password)
		login(self.request, user)
		return valid
	
class LoginView(FormView):
	form_class = AuthenticationForm
	template_name = 'webinterface/login.html'
	
	success_url = reverse_lazy('webinterface:dashboard')
	
	def form_valid(self, form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
	
		if user is not None and user.is_active:
			# login the user
			login(self.request, user)
			
			return super(LoginView, self).form_valid(form)
		else:
			return self.form_invalid(form)
			
class LogoutView(RedirectView):
	url = reverse_lazy('webinterface:index')

	def get(self, request, *args, **kwargs):
		logout(request)
		return super(LogoutView, self).get(request, *args, **kwargs)
		
class DashboardView(TemplateView):
	template_name = 'webinterface/dashboard.html'

	def get(self,request):
		tokens = Token.objects.filter(user=request.user)
		
		context = {}
		context['tokens'] = tokens
		context['problem'] = '{\n\t"variables":[],\n\t"parameters":[],\n\t"constraints":[],\n\t"objective":[]\n}'
		context['response'] = ''
		
		return render(request,self.template_name,context)
		
	def post(self,request):
		context = {}
		
		# get the problem from the request
		problem = request.POST['problem']
		token = request.POST['token']
		
		# call the api
		data = urlencode({'problem': problem }).encode('UTF-8')
		url = Request('http://localhost:8000/api/{}/'.format(token), data)
		response = urlopen(url).read().decode('utf8', 'ignore')
		
		
		tokens = Token.objects.filter(user=request.user)
		
		context = {}
		context['tokens'] = tokens
		context['problem'] = problem
		context['response'] = response
		
		return render(request,self.template_name,context)
