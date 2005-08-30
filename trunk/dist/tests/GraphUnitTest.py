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
from pbnt import Graph
from pbnt.GraphExceptions import *

class TopoSortTestCase(unittest.TestCase):
    def setUp(self):
        a = Node.DirectedNode(1)
        b = Node.DirectedNode(2)
        c = Node.DirectedNode(3)
        d = Node.DirectedNode(4)
        e = Node.DirectedNode(5)
        
        a.add_child(b)
        a.add_child(c)
        b.add_parent(a)
        c.add_parent(a)
        d.add_child(b)
        b.add_parent(d)
        e.add_child(a)
        a.add_parent(e)
        
        self.nodes = [a,b,c,d,e]
    
    def testBasicSetIndex(self):
        """ Test that indices are correct relative to each other, using very basic network structure
        """
        self.graph = Graph.DAG(self.nodes)
        assert(self.nodes[0].index > self.nodes[4].index and \
               self.nodes[1].index > self.nodes[0].index and \
               self.nodes[1].index > self.nodes[3].index and \
               self.nodes[2].index > self.nodes[0].index), \
              "Indexes were not set properly in DAG.topological_sort()"
    
    def testAllIndexSet(self):
        """ Test that all indices are >= 0
        """
        self.graph = Graph.DAG(self.nodes)
        for node in self.nodes:
            assert(node.index >= 0), "Index was less than 0"
    
    def testRaiseCyclicException(self):
        """ Test that the cyclic graph raises an exception.
        """
        self.nodes[0].add_child(self.nodes[4])
        self.nodes[4].add_parent(self.nodes[0])
        self.assertRaises(BadGraphStructure, Graph.DAG, self.nodes)

suite = unittest.makeSuite(TopoSortTestCase, 'test')
runner = unittest.TextTestRunner()
runner.run(suite)

if __name__ == "__main__":
    unittest.main()