
from .models import Token

import parsenlp
import json
import time

def ipopt(token,json_problem):
	# check the token
	try:
		token = Token.objects.get(token=token)
	except:
		response = 'Invalid token'
	else:
		# reset the computation limit if the last call was before today 00h00
		token.check_reset_used_computation_time()
		
		# check the computation time limit
		if token.used_computation_time > token.daily_computation_time:
			response = 'Limit exeeded'
		else:
			start = time.time()
						
			try:
				problem = parsenlp.Problem(json_problem)
			except:
				response = 'There was a problem parsing the problem, check your code'
			else:				
				# check the computation time
				end = time.time()
				
				if token.used_computation_time + int( end-start ) > token.daily_computation_time:
					response = 'Limit exeeded during this call'
				else:
					# solve and get the solution
					try:
						problem.solve()
						sol = problem.get_value_dict()

						# convert numpy arrays to lists
	 					sol = {k:sol[k].tolist() for k in sol.keys()}

						response = json.dumps(sol)
					except:
						response = 'Problem during the solution of the problem. Check your problem and contact the administrator.'
	
	
			# update the computation time
			end = time.time()

			token.used_computation_time += int( end-start )
			token.save()
	
			# check if the limit was not exceeded
			if token.used_computation_time > token.daily_computation_time:
				response = 'Limit exeeded during this call'
				
	return response
