#!/usr/bin/env python

import json
try:
	# python 3 imports
	from urllib.parse import urlencode
	import urllib.request as request
except:
	# python 2 imports
	from urllib import urlencode
	import urllib2 as request
	
	
# load the problem from a file in json format
with open('hs071.json', 'r') as jsonfile:
	problemstring=jsonfile.read().replace('\n', '').replace('\t', ' ')
	
# prepare the data and make a post request	
token = '37f2260f7c2f0bce704672be0274feca30b7b6e2' # fill in a valid token here
data = urlencode({'problem': problemstring }).encode('UTF-8')
url = request.Request('http://webopt.duckdns.org/api/{}/'.format(token), data)

# handle the response
responseData = request.urlopen(url).read().decode('utf8', 'ignore')
print( responseData )
	
