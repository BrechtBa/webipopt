from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy

from .models import Token
from .solver import solve

import parsenlp
import json
import time

@csrf_exempt
def index(request,token):
	
	if token=='':
		response = 'No token supplied'
	elif not 'problem' in request.POST:
		response = 'No problem supplied'
	else:
		json_problem = request.POST['problem']
		response = solve(token,json_problem)
		
				
		
	return HttpResponse( response )
