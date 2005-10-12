# PBNT: Python Bayes Network Toolbox
#
# Copyright (c) 2005, Elliot Cohen
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
# * The name "Elliot Cohen" may not be used to endorse or promote
#   products derived from this software without specific prior written
#   permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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

class DBNTestCase(unittest.TestCase):
    def setUp(self):
        """ Create a 1.5 slice specification of a DBN.
        """
        rain = Node.DynamicNode(1,2,tSlice=ABSTRACTSLICE,name="Rain")
        umbrella = Node.DynamicNode(2,2,tSlice=ABSTRACTSLICE,name="Umbrella")
        # Specify graph structure
        rain.add_child(umbrella)
        umbrella.add_parent(rain)
        # Specify temporal structure
        rain.add_next_slice(rain)
        rain.add_prev_slice(rain)
        self.nodes = [rain,umbrella]
        self.DBN = Graph.DBN(self.nodes)
    
    def testBasicDBN(self):
        """ Sanity check that DBN was basically created correctly.
        """
        for node in self.DBN.nodes:
            if node == self.nodes[0]:
                assert(node.children == set([self.nodes[1]]) and \
                       node.parents == set() and \
                       node.tparents == set([node]) and \
                       node.tchildren == set([node])), \
                      "BasicDBN: Rain's connections are malformed"
            if node == self.nodes[1]:
                assert(node.children == set() and \
                       node.parents == set([self.nodes[0]]) and \
                       node.tchildren == set() and \
                       node.tparents == set()), \
                      "BasicDBN: Umbrella's connections are malformed"
    
    def testUnroll(self):
        """ Test that the graph is unrolled appropriately.
        """
        g = unroll(self.DBN, 3)
        rain = self.nodes[0]
        umbrella = self.nodes[1]
        rain0 = copy.copy(rain)
        rain0.tSlice = 0
        rain1 = copy.copy(rain)
        rain1.tSlice = 1
        rain2 = copy.copy(rain)
        rain2.tSlice = 2
        umbrella0 = copy.copy(umbrella)
        umbrella0.tSlice = 0
        umbrella1 = copy.copy(umbrella)
        umbrella1.tSlice = 1
        umbrella2 = copy.copy(umbrella)
        umbrella2.tSlice = 2
        success = True
        for node in g.nodes:
            if node.tSlice == 0:
                if node.id == 1:
                    success == (node.parents == set() and \
                                node.children == set([umbrella0, rain1]))
                if node.id == 2:
                    success == (node.parents == set([rain0]) and \
                                node.children == set())
            if node.tSlice == 1:
                if node.id == 1:
                    success == (node.parents == set([rain0]) and \
                                node.children == set([rain2, umbrella1]))
                if node.id == 2:
                    success == (node.parents == set([rain1]) and \
                                node.children == set())
            if node.tSlice == 2:
                if node.id == 1:
                    success == (node.parents == set([rain1]) and \
                                node.children == set([umbrella2]))
                if node.id == 2:
                    success == (node.parents == set([rain2]) and \
                                node.children == set())
        assert(success == True), "UnrollDBN: structure of unrolled network incorrect"
    
                
                    
               
               
suite = unittest.makeSuite(TopoSortTestCase, 'test')
runner = unittest.TextTestRunner()
runner.run(suite)

suite2 = unittest.makeSuite(DBNTestCase, 'test')
runner2 = unittest.TextTestRunner()
runner2.run(suite2)

if __name__ == "__main__":
    unittest.main()
