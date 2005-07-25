from BayesNet import *
from DiscreteDistribution import *
from numarray import *
import numarray.objects as obj 
 
 
def water():
 
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
  cDistribution = DiscreteDistribution(array([0.5, 0.5], type=Float), nodeSizes[cloudy])
  
  #sprinkler
  dist = zeros([nodeSizes[cloudy],nodeSizes[sprinkler]], type=Float)
  dist[0,] = 0.5
  dist[1,] = [0.9,0.1]
  sDistribution = DiscreteDistribution(dist, nodeSizes[sprinkler])
  
  #rain
  dist = zeros([nodeSizes[cloudy], nodeSizes[rain]], type=Float)
  dist[0,] = [0.8,0.2]
  dist[1,] = [0.2,0.8]
  rDistribution = DiscreteDistribution(dist, nodeSizes[rain])
  
  #wetgrass
  dist = zeros([nodeSizes[sprinkler], nodeSizes[rain], nodeSizes[wetgrass]], type=Float)
  dist[0,0,] = [1.0,0.0]
  dist[1,0,] = [0.1,0.9]
  dist[0,1,] = [0.1,0.9]
  dist[1,1,] = [0.01,0.99]
  wgDistribution = DiscreteDistribution(dist, nodeSizes[wetgrass])
  
  distributions = obj.array([cDistribution, sDistribution, rDistribution, wgDistribution])
  
  #create bayes net
  bnet = BayesNet(adjMat, nodeSizes, distributions)
  
  return bnet
