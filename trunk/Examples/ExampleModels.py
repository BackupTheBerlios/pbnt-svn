from BayesNet import *
from DiscreteDistribution import *
from numarray import *
from BayesNode import *
import numarray.objects as obj 
 
 
def water():
 
 #testing basic bayes net class implementation
  numberOfNodes = 4
  #name the nodes
  cloudy = 0
  sprinkler = 1
  rain = 2
  wetgrass = 3
  
  cNode = BayesNode( 2, 0, "cloudy" )
  sNode = BayesNode( 2, 1, "sprinkler" )
  rNode = BayesNode( 2, 2, "rain" )
  wNode = BayesNode( 2, 3, "wetgrass" )

  #cloudy
  cNode.addChild( sNode )
  cNode.addChild( rNode )
  
  #sprinkler
  sNode.addParent( cNode )
  sNode.addChild( wNode )
  
  #rain 
  rNode.addParent( cNode )
  rNode.addChild( wNode )
  
  #wetgrass
  wNode.addParent( sNode )
  wNode.addParent( rNode )
  
  nodes = [cNode, sNode, rNode, wNode]
  
  #create distributions
  #cloudy distribution
  cDistribution = DiscreteDistribution(array([0.5, 0.5], type=Float32), cNode.nodeSize)
  cNode.setCPT( cDistribution )
  
  #sprinkler
  dist = zeros([cNode.nodeSize,sNode.nodeSize], type=Float32)
  dist[0,] = 0.5
  dist[1,] = [0.9,0.1]
  sDistribution = DiscreteDistribution(dist, sNode.nodeSize)
  sNode.setCPT( sDistribution )
  
  #rain
  dist = zeros([cNode.nodeSize, rNode.nodeSize], type=Float32)
  dist[0,] = [0.8,0.2]
  dist[1,] = [0.2,0.8]
  rDistribution = DiscreteDistribution(dist, rNode.nodeSize)
  rNode.setCPT( rDistribution )
  
  #wetgrass
  dist = zeros([sNode.nodeSize, rNode.nodeSize, wNode.nodeSize], type=Float32)
  dist[0,0,] = [1.0,0.0]
  dist[1,0,] = [0.1,0.9]
  dist[0,1,] = [0.1,0.9]
  dist[1,1,] = [0.01,0.99]
  wgDistribution = DiscreteDistribution(dist, wNode.nodeSize)
  wNode.setCPT( wgDistribution )
  
  
  #create bayes net
  bnet = BayesNet( nodes )
  
  return bnet
