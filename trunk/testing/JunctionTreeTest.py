#don't have to import BayesNet, DiscreteDistribution, 
#or numarray because it is done in ExampleModels
import ExampleModels as EX
from JunctionTreeEngine import *
from utilities import *

def test():
	
	
	#define water network
	water = EX.water()
	
	#define variable indexes
	cloudy = 0
	sprinkler = 1
	rain = 2
	wetgrass = 3
	
	engine = JunctionTreeEngine(water)
	
	test0 = 1
	
	Q = engine.marginal([water.nodes[sprinkler]])[0]
	
	if allclose(Q.CPT[False], .7, atol=.0001):
		print "Test 0A: OK\n"
	else:
		test0 = 0
		print "Test 0A: FAILED\n"
	
	if allclose(Q.CPT[True], .3, atol=.0001):
		print "Test 0B: OK\n"
	else:
		test0 = 0
		print "Test 0B: FAILED\n"
	
	engine.add_evidence(cloudy, False)
	engine.add_evidence(rain, True)
	
	Q = engine.marginal([water.nodes[wetgrass]])[0]
	
	test1 = 1
	if alltrue(engine.evidence == array([0,-1,1,-1])):
		print "Test 1: OK\n"
	else:
		test1 = 0
		print "Test 1: FAILED\n"
	
	#these are the values of wetgrass according to Kevin Murphys FullBNT
	test2 = 1
	#don't know how to handle floating point differences so use hack for now
	if allclose(Q.CPT[False], .0550, atol=.0001):
		print "Test 2A: OK\n"
	else:
		test2 = 0
		print "Test 2A: FAILED\n"
	
	if allclose(Q.CPT[True], .9450, atol=.0001):
		print "Test 2B: OK\n"
	else:
		test2 = 0
		print "Test 2B: FAILED\n"
	
	Q = engine.marginal([water.nodes[sprinkler]])[0]
	
	test3 = 1
	if allclose(Q.CPT[False], .5, atol=.0001):
		print "Test 3A: OK\n"
	else:
		test3 = 0
		print "Test 3A: FAILED\n"
	
	if allclose(Q.CPT[True], .5, atol=.0001):
		print "Test 3B: OK\n"
	else:
		test3 = 0
		print "Test 3B: FAILED\n"
	
	
	engine.add_evidence(cloudy, -1)
	engine.add_evidence(sprinkler, 0)
	engine.add_evidence(wetgrass, 1)
	
	Q = engine.marginal([water.nodes[cloudy]])[0]
	
	test4 = 1
	if allclose(Q.CPT[False], .1220, atol=.0001):
		print "Test 4A: OK\n"
	else:
		test4 = 0
		print "Test 4A: FAILED\n"
	
	if allclose(Q.CPT[True], .8780, atol=.0001):
		print "Test 4B: OK\n"
	else:
		test4 = 0
		print "Test 4B: FAILED\n"
	
	Q = engine.marginal([water.nodes[rain]])[0]
	
	test5 = 1
	if allclose(Q.CPT[False], 0, atol=.0001):
		print "Test 5A: OK\n"
	else:
		test5 = 0
		print "Test 5A: FAILED\n"
	
	if allclose(Q.CPT[True], 1, atol=.0001):
		print "Test 5B: OK\n"
	else:
		test5 = 0
		print "Test 5B: FAILED\n"
	
	return array([test1,test2,test3,test4,test5])
	

def testMoral():
		#define water network
	water = EX.water()
	
	#define variable indexes
	cloudy = 0
	sprinkler = 1
	rain = 2
	wetgrass = 3
	
	engine = JunctionTreeEngine(water)
	
	moral = engine.moralGraph()
	
	correctMoral = water.graph.copy()
	
	#first make undirected
	correctMoral[sprinkler,cloudy] = 1
	correctMoral[rain, cloudy] = 1
	correctMoral[wetgrass,sprinkler] = 1
	correctMoral[wetgrass,rain] = 1
	
	#now connect the parents of each node
	#cloudy has no parents
	#sprinkler has only one parent
	#rain has only one parent
	#wetgrass has two parents rain and sprinkler, so connect them
	correctMoral[sprinkler,rain] = 1
	correctMoral[rain, sprinkler] = 1
	
	test1 = 1
	if alltrue(moral == correctMoral):
		print "Test 1: OK\n"
	else:
		test1 = 0
		print "Test 1: FAILED\n"
	
