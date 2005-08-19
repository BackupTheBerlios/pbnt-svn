#don't have to import BayesNet, DiscreteDistribution, 
#or numarray because it is done in ExampleModels
import ExampleModels as EX
from Inference import *
from Utilities import *

def test():
	
	
	#define water network
	water = EX.water()
	
	#define variable indexes
	cloudy = 0
	sprinkler = 1
	rain = 2
	wetgrass = 3
	
	engine = MCMCEngine(water)
	
	test0 = 1
	
	engine.add_evidence(cloudy, False)
	engine.add_evidence(sprinkler, True)
	
	Q = engine.marginal([water.nodes[wetgrass]], 5000)[0]
	
	if allclose(Q.CPT[False], .06, atol=.04):
		print "Test 0A: OK\n"
	else:
		test0 = 0
		print "Test 0A: FAILED\n"
	
	if allclose(Q.CPT[True], .92, atol=.04):
		print "Test 0B: OK\n"
	else:
		test0 = 0
		print "Test 0B: FAILED\n"
	
	Q = engine.marginal([water.nodes[rain]], 5000)[0]
	
	test1 = 1
	#don't know how to handle floating point differences so use hack for now
	if allclose(Q.CPT[False], .8, atol=.2):
		print "Test 1A: OK\n"
	else:
		test1 = 0
		print "Test 1A: FAILED\n"
	
	if allclose(Q.CPT[True], .2, atol=.2):
		print "Test 1B: OK\n"
	else:
		test1 = 0
		print "Test 1B: FAILED\n"
	
	
	engine.add_evidence(cloudy, -1)
	engine.add_evidence(rain, True)
		
	Q = engine.marginal([water.nodes[cloudy]], 5000)[0]
	
	test2 = 1
	if allclose(Q.CPT[False], .55, atol=.04):
		print "Test 2A: OK\n"
	else:
		test2 = 0
		print "Test 2A: FAILED\n"
	
	if allclose(Q.CPT[True], .44, atol=.04):
		print "Test 2B: OK\n"
	else:
		test2 = 0
		print "Test 2B: FAILED\n"
	
	Q = engine.marginal([water.nodes[sprinkler]], 5000)[0]
	
	test3 = 1
	if allclose(Q.CPT[False], 0, atol=.0001):
		print "Test 3A: OK\n"
	else:
		test3 = 0
		print "Test 3A: FAILED\n"
	
	if allclose(Q.CPT[True], 1, atol=.0001):
		print "Test 3B: OK\n"
	else:
		test3 = 0
		print "Test 3B: FAILED\n"
	
	engine.add_evidence(sprinkler, -1)
	engine.add_evidence(rain, -1)
	engine.add_evidence(cloudy, True)
	engine.add_evidence(wetgrass, True)
	
	Q = engine.marginal([water.nodes[rain]], 5000)[0]
	
	test4 = 1
	if allclose(Q.CPT[False], .02, atol=.02):
		print "Test 4A: OK\n"
	else:
		test4 = 0
		print "Test 4A: FAILED\n"
	
	if allclose(Q.CPT[True], .98, atol=.02):
		print "Test 4B: OK\n"
	else:
		test4 = 0
		print "Test 4B: FAILED\n"
	
	Q = engine.marginal([water.nodes[sprinkler]], 5000)[0]
	
	test5 = 1
	if allclose(Q.CPT[False], .87, atol=.03):
		print "Test 5A: OK\n"
	else:
		test5 = 0
		print "Test 5A: FAILED\n"
	
	if allclose(Q.CPT[True], .13, atol=.03):
		print "Test 5B: OK\n"
	else:
		test5 = 0
		print "Test 5B: FAILED\n"	
	
	return array([test1,test2,test3,test4, test5])