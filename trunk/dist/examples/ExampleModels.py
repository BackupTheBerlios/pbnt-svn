import numarray.objects as obj
from Graph import *
from Distribution import *
from numarray import *
from Node import *
    
def water():
    
    #testing basic bayes net class implementation
    numberOfNodes = 4
    #name the nodes
    cloudy = 0
    sprinkler = 1
    rain = 2
    wetgrass = 3
    
    cNode = BayesNode(0, 2, index=0, name="cloudy")
    sNode = BayesNode(1, 2, index=1, name="sprinkler")
    rNode = BayesNode(2, 2, index=2, name="rain")
    wNode = BayesNode(3, 2, index=3, name="wetgrass")

    #cloudy
    cNode.add_child(sNode)
    cNode.add_child(rNode)
    
    #sprinkler
    sNode.add_parent(cNode)
    sNode.add_child(wNode)
    
    #rain 
    rNode.add_parent(cNode)
    rNode.add_child(wNode)
    
    #wetgrass
    wNode.add_parent(sNode)
    wNode.add_parent(rNode)
    
    nodes = [cNode, sNode, rNode, wNode]
    
    #create distributions
    #cloudy distribution
    cDistribution = DiscreteDistribution(cNode)
    index = cDistribution.generate_index([],[])
    cDistribution[index] = 0.5
    cNode.set_dist(cDistribution)
    
    #sprinkler
    dist = zeros([cNode.size(),sNode.size()], type=Float32)
    dist[0,] = 0.5
    dist[1,] = [0.9,0.1]
    sDistribution = ConditionalDiscreteDistribution(nodes=[cNode, sNode], table=dist)
    sNode.set_dist(sDistribution)
    
    #rain
    dist = zeros([cNode.size(), rNode.size()], type=Float32)
    dist[0,] = [0.8,0.2]
    dist[1,] = [0.2,0.8]
    rDistribution = ConditionalDiscreteDistribution(nodes=[cNode, rNode], table=dist)
    rNode.set_dist(rDistribution)
    
    #wetgrass
    dist = zeros([sNode.size(), rNode.size(), wNode.size()], type=Float32)
    dist[0,0,] = [1.0,0.0]
    dist[1,0,] = [0.1,0.9]
    dist[0,1,] = [0.1,0.9]
    dist[1,1,] = [0.01,0.99]
    wgDistribution = ConditionalDiscreteDistribution(nodes=[sNode, rNode, wNode], table=dist)
    wNode.set_dist(wgDistribution)
    
    
    #create bayes net
    bnet = BayesNet(nodes)
    
    return bnet

