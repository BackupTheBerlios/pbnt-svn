from numarray import *
import numarray.objects as obj
from BayesNet import *
from DiscreteDistribution import *

def test():
  #testing basic bayes net class implementation
  numberOfNodes = 4
  #name the nodes
  cloudy = 0
  sprinkler = 1
  rain = 2
  wetgrass = 3
  
  #create adjacency matrix
  adjMat = zeros([numberOfNodes, numberOfNodes], type=Bool)
  
  #we can specify parent child combinations by making two lists one of the parents and another of the children
  parents = [cloudy, cloudy, sprinkler, rain]
  children = [sprinkler, rain, wetgrass, wetgrass]
  
  #specify the size of each node
  nodeSizes = array([2,2,2,2])
  
  adjMat[parents, children] = 1

  #create distributions
  #cloudy distribution
  cDistribution = DiscreteDistribution(array([0.5, 0.5], type=Float32), nodeSizes[cloudy])
  
  #sprinkler
  dist = zeros([nodeSizes[cloudy],nodeSizes[sprinkler]], type=Float32)
  dist[0,] = 0.5
  dist[1,] = [0.9,0.1]
  sDistribution = DiscreteDistribution(dist, nodeSizes[sprinkler])
  
  #rain
  dist = zeros([nodeSizes[cloudy], nodeSizes[rain]], type=Float32)
  dist[0,] = [0.8,0.2]
  dist[1,] = [0.2,0.8]
  rDistribution = DiscreteDistribution(dist, nodeSizes[rain])
  
  #wetgrass
  dist = zeros([nodeSizes[sprinkler], nodeSizes[rain], nodeSizes[wetgrass]], type=Float32)
  dist[0,0,] = [1.0,0.0]
  dist[1,0,] = [0.1,0.9]
  dist[0,1,] = [0.1,0.9]
  dist[1,1,] = [0.01,0.99]
  wgDistribution = DiscreteDistribution(dist, nodeSizes[wetgrass])
  
  distributions = obj.array([cDistribution, sDistribution, rDistribution, wgDistribution])
  
  #create bayes net
  bnet = BayesNet(adjMat, nodeSizes, distributions)
  
  #test that it was created
  print bnet.graph
  test1 = 1
  print "test 1: OK\n"
  
  #test that it is the same
  test2 = 1
  if all(bnet.graph == adjMat):
    print "test 2: OK\n"
  else:
    test2 = 0
    print "test 2: FAILED\n"
  
  #test that the nodeSizes are the same
  ns = bnet.nodeSizes
  test3 = 1
  if size(ns) != size(nodeSizes):
    test3 = 0
  
  for i in range(len(ns)):
    if ns[i] != nodeSizes[i]:
      test3 = 0
  
  if test3:
    print "test 3: OK\n"
  else:
    print "test 3: FAILED\n"
  
  
  #now we are going to check parent and child functions
  cparents = bnet.parents(cloudy)
  cchildren = bnet.children(cloudy)
  
  sparents = bnet.parents(sprinkler)
  schildren = bnet.children(sprinkler)
  
  rparents = bnet.parents(rain)
  rchildren = bnet.children(rain)
  
  wgparents = bnet.parents(wetgrass)
  wgchildren = bnet.children(wetgrass)
  
  #test cloudy
  test4 = 1
  if size(cparents) == 0:
    print "\ttest 4a: OK\n"
  else:
    test4 = 0
    print "\ttest 4a: FAILED\n"
  
  if size(cchildren) == 2 and cchildren[0] == sprinkler and cchildren[1] == rain:
    print "\ttest 4b: OK\n"
  else:
    test4 = 0
    print "\ttest 4b: FAILED\n"
  
  if test4:
    print "test 4: OK\n"
  else:
    print "test 4: FAILED\n"
  
  #test sprinkler
  test5 = 1
  if size(sparents) == 1 and sparents[0] == cloudy:
    print "\ttest 5a: OK\n"
  else:
    test5 = 0
    print "\ttest 5a: FAILED\n"
  
  if size(schildren) == 1 and schildren[0] == wetgrass:
    print "\ttest 5b: OK\n"
  else:
    test5 = 0
    print "\ttest 5b: FAILED\n"
  
  if test5:
    print "test 5: OK\n"
  else:
    print "test 5: FAILED\n"
    
  
  #test rain
  test6 = 1
  if size(rparents) == 1 and rparents[0] == cloudy:
    print "\ttest 6a: OK\n"
  else:
    test6 = 0
    print "\ttest 6a: FAILED\n"
  
  if size(rchildren) == 1 and rchildren[0] == wetgrass:
    print "\ttest 6b: OK\n"
  else:
    test6 = 0
    print "\ttest 6b: FAILED\n"
  
  if test6:
    print "test 6: OK\n"
  else:
    print "test 6: FAILED\n"
  
  
  #test wetgrass
  test7 = 1
  if size(wgparents) == 2 and wgparents[0] == sprinkler and wgparents[1] == rain:
    print "\ttest 7a: OK\n"
  else:
    test7 = 0
    print "\ttest 7a: FAILED\n"
  
  if size(wgchildren) == 0:
    print "\ttest 7b: OK\n"
  else:
    test7 = 0
    print "\ttest 7b: FAILED\n"
  
  if test7:
    print "test 7: OK\n"
  else:
    print "test 7: FAILED\n"
    
  
  #test distributions
  cloudyVal = 0
  test8 = 1
  if bnet.CPTs[cloudy].probabilityOf(array([cloudyVal])) == 0.5:
    print "test 8a: OK\n"
  else:
    test8 = 0
    print "test 8a: FAILED\n"
    
  rainVal = 1
  if bnet.CPTs[rain].probabilityOf(array([cloudyVal, rainVal])) == 0.2:
    print "test 8b: OK\n"
  else:
    test8 = 0
    print "test 8b: FAILED\n"
  
  sprinklerVal = 0
  if bnet.CPTs[sprinkler].probabilityOf(array([cloudyVal, sprinklerVal])) == 0.5:
    print "test 8c: OK\n"
  else:
    test8 = 0
    print "test 8c: FAILED\n"
                                  
  wetgrassVal = 1
  if bnet.CPTs[wetgrass].probabilityOf(array([sprinklerVal, rainVal, wetgrassVal])) == 0.9:
    print "test 8d: OK\n"
  else:
    test8 = 0
    print "test 8d: FAILED\n"
    
  return array([test1,test2,test3,test4,test5,test6,test7,test8])
