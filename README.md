# webopt
Web API and interface for cloud based solving or non-linear optimization problems using using ipopt

## demo
An online version can be found at [webopt.duckdns.org](http://webopt.duckdns.org).
Tokens with 10 minutes daily computation time can be obtained for free by registering.

## problem submission
Optimization problems must be submitted in an easy to read json format parsable by `parsenlp`. An example is given below for the Hock - Schittkowski model 71.
```
{
	"variables":[
		"x[j] for j in range(4)"
	],
	"parameters": [
		"A = 25",
		"B = 40",
		"C = 1",
		"D = 5"
	],
	"objective": 
		"x[0]*x[3]*(x[0]+x[1]+x[2])+x[2]",
	"constraints":[
		"x[0]*x[1]*x[2]*x[3] >= A",
		"x[0]**2+x[1]**2+x[2]**2+x[3]**2 = B",
		"x[j] >= C for j in range(4)",
		"x[j] <= D for j in range(4)"
	]
}
```

## api
Optimization problems can be submitted through the api using a http POST request.
This can be used in your own web apps.

An example of using python to call the api is given [here](https://github.com/BrechtBa/webopt/tree/master/examples/api_example.py). 
