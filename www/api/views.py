from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from customauth.models import User

import parsenlp
import json
import time

@csrf_exempt
def index(request,token):

	response = token
	
	if token=='':
		response = 'No token supplied'
	else:
		# check the token
		computation_permitted = True;
		try:
			user = User.objects.get(token=token)
			
			# reset the computation limit if the last call was before today 00h00
			print( user.last_api_call )
			print( timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) )
			if user.last_api_call < timezone.now().replace(hour=0, minute=0, second=0, microsecond=0):
				user.used_computation_time = 0
			
			# check the computation time limit
			if user.used_computation_time > user.daily_computation_time:
				computation_permitted = False
				response = 'Limit exeeded'
		except:
			computation_permitted = False
			response = 'Invalid token'
			
			
		start = time.time()
		
		if computation_permitted:
			if 'problem' in request.POST:
				json_problem = request.POST['problem']
				
				problem = parsenlp.Problem(json_problem)
				
				# solve and get the solution
				#problem.solve()
				#sol = problem.get_value_dict()
				solution = {'time': [1,2,3,4,5], 'x': [3,4,5,4,3], 'y': [4,5,6,6,6]}
				
				response = json.dumps(solution)

			else:
				response = 'No problem supplied'
	
		# update the computation time
		end = time.time()
		user.used_computation_time += int( end-start )
		user.save()
		
		# check if the limit was not exceeded
		if user.used_computation_time > user.daily_computation_time:
			response = 'Limit exeeded during this call'
		
	return HttpResponse( response )
