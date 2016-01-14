from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import parsenlp
import json

@csrf_exempt
def index(request,token):

	response = token
	
	if token=='':
		response = 'No token supplied'
	else:
		# check the token
		valid_token = True;
		if False:
			valid_token = False
			response = 'Invalid token'
			
		if False:
			valid_token = False
			response = 'Limit exeeded'	

			
		if valid_token:
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
	
		
	return HttpResponse( response )
