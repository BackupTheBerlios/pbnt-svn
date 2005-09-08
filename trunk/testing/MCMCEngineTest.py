#don't have to import BayesNet, DiscreteDistribution, 
#or numarray because it is done in ExampleModels
import sys
sys.path.append('../dist/lib')
sys.path.append('../dist')
import examples.ExampleModels as EX
from pbnt.Inference import *
from pbnt.Utilities import *

def test():
    
    
    #define water network
    water = EX.water()
    
    #define variable indexes
    for node in water.nodes:
        if node.id == 0:
            cloudy = node
        if node.id == 1:
            sprinkler = node
        if node.id == 2:
            rain = node
        if node.id == 3:
            wetgrass = node
    
    engine = MCMCEngine(water)
    
    test0 = 1
    
    engine.evidence[cloudy] = False
    engine.evidence[sprinkler] = True
    
    Q = engine.marginal(wetgrass, 5000)[0]
    index = Q.generate_index([False], range(Q.nDims))
    if allclose(Q[index], .06, atol=.04):
        print "Test 0A: OK\n"
    else:
        test0 = 0
        print "Test 0A: FAILED\n"
    index = Q.generate_index([True], range(Q.nDims))
    if allclose(Q[index], .92, atol=.04):
        print "Test 0B: OK\n"
    else:
        test0 = 0
        print "Test 0B: FAILED\n"
    
    Q = engine.marginal(rain, 5000)[0]
    
    test1 = 1
    #don't know how to handle floating point differences so use hack for now
    index = Q.generate_index([False], range(Q.nDims))
    if allclose(Q[index], .8, atol=.2):
        print "Test 1A: OK\n"
    else:
        test1 = 0
        print "Test 1A: FAILED\n"
    index = Q.generate_index([True], range(Q.nDims))
    if allclose(Q[index], .2, atol=.2):
        print "Test 1B: OK\n"
    else:
        test1 = 0
        print "Test 1B: FAILED\n"
    
    
    engine.evidence[cloudy] = -1
    engine.evidence[rain] = True
        
    Q = engine.marginal(cloudy, 5000)[0]
    
    test2 = 1
    index = Q.generate_index([False], range(Q.nDims))
    if allclose(Q[index], .55, atol=.04):
        print "Test 2A: OK\n"
    else:
        test2 = 0
        print "Test 2A: FAILED\n"
    index = Q.generate_index([True], range(Q.nDims))
    if allclose(Q[index], .44, atol=.04):
        print "Test 2B: OK\n"
    else:
        test2 = 0
        print "Test 2B: FAILED\n"
    
    Q = engine.marginal(sprinkler, 5000)[0]
    
    test3 = 1
    index = Q.generate_index([False], range(Q.nDims))
    if allclose(Q[index], 0, atol=.0001):
        print "Test 3A: OK\n"
    else:
        test3 = 0
        print "Test 3A: FAILED\n"
    index = Q.generate_index([True], range(Q.nDims))
    if allclose(Q[index], 1, atol=.0001):
        print "Test 3B: OK\n"
    else:
        test3 = 0
        print "Test 3B: FAILED\n"
    
    engine.evidence[sprinkler] = -1
    engine.evidence[rain] = -1
    engine.evidence[cloudy] = True
    engine.evidence[wetgrass] = True
    
    Q = engine.marginal(rain, 5000)[0]
    
    test4 = 1
    index = Q.generate_index([False], range(Q.nDims))
    if allclose(Q[index], .02, atol=.02):
        print "Test 4A: OK\n"
    else:
        test4 = 0
        print "Test 4A: FAILED\n"
    index = Q.generate_index([True], range(Q.nDims))
    if allclose(Q[index], .98, atol=.02):
        print "Test 4B: OK\n"
    else:
        test4 = 0
        print "Test 4B: FAILED\n"
    
    Q = engine.marginal(sprinkler, 5000)[0]
    
    test5 = 1
    index = Q.generate_index([False], range(Q.nDims))
    if allclose(Q[index], .87, atol=.03):
        print "Test 5A: OK\n"
    else:
        test5 = 0
        print "Test 5A: FAILED\n"
    
    index = Q.generate_index([True], range(Q.nDims))
    if allclose(Q[index], .13, atol=.03):
        print "Test 5B: OK\n"
    else:
        test5 = 0
        print "Test 5B: FAILED\n"	
    
    return array([test1,test2,test3,test4, test5])
