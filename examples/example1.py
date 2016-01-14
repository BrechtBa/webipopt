#!/usr/bin/env python3

import urllib.parse
import urllib.request
import json


# load the problem from a file in json format
with open('example1.json', 'r') as jsonfile:
    problemstring=jsonfile.read().replace('\n', '').replace('\t', ' ')
	

# prepare the data and make a post request	
token = 'abcd0.123='
data = urllib.parse.urlencode({'problem': problemstring }).encode('UTF-8')
url = urllib.request.Request('http://localhost:8000/api/{}/'.format(token), data)


# handle the response
responseData = urllib.request.urlopen(url).read().decode('utf8', 'ignore')
print( responseData )