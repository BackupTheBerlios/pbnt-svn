#!/usr/bin/env python
# Builtin Python Libraries
import sys
import unittest
# Major Packages
import numarray
# Assume we are in dist/tests directory
sys.path.append('../lib')
# Library specific modules
from pbnt import Distribution
from pbnt import Node
from pbnt import Inference

class InferenceTestCase(unittest.TestCase):
    def setUp(self):
        cNode = BayesNode(0, 2, name="cloudy")
        sNode = BayesNode(1, 2, name="sprinkler")
        rNode = BayesNode(2, 2, name="rain")
        wNode = BayesNode(3, 2, name="wetgrass")
        
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
        
        self.nodes = [cNode, sNode, rNode, wNode]
        
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
        self.bnet = BayesNet(self.nodes)
        self.engine = Inference.InferenceEngine(self.bnet)
    
    def testBlankEvidence(self):
        nonEvidence = self.engine.empty_evidence()
        assert(set(nonEvidence) == set(self.nodes))
    
    def testInsertEvidence(self):
        node = self.nodes[2]
        self.engine.evidence[node] = 1
        nonEvidence = self.engine.empty_evidence()
        nodes = set([self.nodes[0], self.nodes[1], self.nodes[3]])
        assert(set(nonEvidence) == nodes)
    
suite = unittest.makeSuite(InferenceTestCase, 'test')
runner = unittest.TextTestRunner()
runner.run(suite)

if __name__ == "__main__":
    unittest.main()