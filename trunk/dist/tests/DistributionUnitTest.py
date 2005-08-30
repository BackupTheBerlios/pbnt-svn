#!/usr/bin/env python
# Builtin Python Libraries
import sys
import unittest
# Major Packages
from numarray import *
# Assume we are in dist/tests directory
sys.path.append('../lib')
# Library specific modules
from pbnt import Distribution
from pbnt import Node

class PotentialTestCase(unittest.TestCase):
    def setUp(self):
        cNode = Node.BayesNode(0, 2, index=0, name="cloudy")
        sNode = Node.BayesNode(1, 2, index=1, name="sprinkler")
        rNode = Node.BayesNode(2, 2, index=2, name="rain")
        wNode = Node.BayesNode(3, 2, index=3, name="wetgrass")
        self.nodes = [cNode, sNode, rNode, wNode]
        self.potential = Distribution.Potential(self.nodes, default=1)
    
    def testIntMultiply(self):
        assert all(self.potential.table == 1)
        new = self.potential * 4
        assert all(new.table == 4)
        new = self.potential * 4
        assert all(new.table == 4)
        
    def testPotentialEQ(self):
        new = Distribution.Potential(self.nodes)
        assert(self.potential == new)
    
    def testBasicMultiply(self):
        new = self.potential * Distribution.Potential(self.nodes[1:3], default=3)
        # This just checks their nodesets are equal
        assert(len(new.nodes) == len(self.potential.nodes))
        # Not Finished
    
    def testIntDiv(self):
        assert all(self.potential.table == 1)
        new = self.potential / 2
        assert all(new.table == 0.5)
        self.potential /= 2
        assert all(self.potential.table == 0.5)
    
    def testBasicDiv(self):
        assert all(self.potential.table == 1)
        other = Distribution.Potential(self.nodes, default=2)
        new = self.potential / other
        assert all(new.table == 0.5)
        assert all(self.potential.table == 1)
        self.potential /= other
        assert all(new.table == 0.5)
    
    #def testTranspose(self):
        #""" Test both the copy and the inplace are working """
        #assert(alltrue(self.potential.table == 1) == True)
        #nodes = [self.nodes[2], self.nodes[1], self.nodes[3], self.nodes[0]]
        #self.potential.table = arange(16, shape=(2,2,2,2))
        #table = arange(16, shape=(2,2,2,2))
        #table.transpose(axis=(2,1,3,0))
        ## Make sure we didn't start out equal, sanity check
        #assert(alltrue(self.potential.table == table) == False)
        #new = Distribution.Potential(nodes, table=table)
        #newTable = new.transpose_copy(self.nodes)
        ## Check if the new table has been transposed correctly
        #assert(alltrue(self.potential.table == newTable) == True)
        ## Make sure we didn't do it in place
        #assert(alltrue(self.potential.table == new.table) == False)
        #new.transpose(self.nodes)
        ## Check if in place transpose worked
        #assert(alltrue(self.potential.table == new.table) == True)

suite = unittest.makeSuite(PotentialTestCase, 'test')
runner = unittest.TextTestRunner()
runner.run(suite)

if __name__ == "__main__":
    unittest.main()
        