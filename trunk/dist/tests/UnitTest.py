# Major packages
from numarray import *

#Local modules
from Node import *
from Graph import *
from Inference import *
import ExampleModels as EX

""" This file is a set of unit tests.  They are all written as separate functions that return true or false.
"""

########################### Test: Moral DBN #################################
def moral_dbn_interface_connected():
    dbn = EX.basic_dbn()
    moral = MoralDBNGraph(dbn)
    
    # Check that forward and backward interfaces are what they should be
    forwardInterface = set()
    backwardInterface = set()
    for node in dbn.nodes:
        if (len(node.parentsT0) > 0):
            backwardInterface.add(node)
        if (len(node.childrenT1) > 0):
            forwardInterface.add(node)
    test1 = 1
    if forwardInterface == moral.forwardInterface:
        print "Test 1: OK"
    else:
        print "Test1: FAILED"
        test1 = 0
    test2 = 1
    if backwardInterface == moral.backwardInterface:
        print "Test 2: OK"
    else:
        print "Test 2: FAILED"
        test2 = 0
    test3 = 1
    for node in forwardInterface:
        forwardInterface.remove(node)
        if not forwardInterface == node.neighborSet:
            test3 = 0
        forwardInterface.add(node)
    if test3:
        print "Test 3: OK"
    else:
        print "Test 3: FAILED"
    test4 = 1
    for node in backwardInterface:
        backwardInterface.remove(node)
        if not backwardInterface == node.neighborSet:
            test4 = 0
        backwardInterface.add(node)
    if test4:
        print "Test 4: OK"
    else:
        print "Test 4: FAILED"
    return (test1 and test2 and test3 and test4)
       

########################### Test: topological sort #################################
def test_topo_sort():
    a = DirectedNode(1)
    b = DirectedNode(2)
    c = DirectedNode(3)
    d = DirectedNode(4)
    e = DirectedNode(5)
    
    a.add_child(b)
    a.add_child(c)
    b.add_parent(a)
    c.add_parent(a)
    d.add_child(b)
    b.add_parent(d)
    e.add_child(a)
    a.add_parent(e)
    
    l = [a,b,c,d,e]
    dag = DAG(l)
    if a.index > e.index and b.index > a.index and b.index > d.index and c.index > a.index:
        test1 = 1
        print "Test1: OK"
    else:
        test1 = 0
        print "Test1: FAILED"
    test2 = 1
    for i in l:
        if i.index == -1:
            test2 = 0
    if test2:
        print "Test2: OK"
    else:
        print "Test2: FAILED"
    # Make graph cyclic
    e.add_parent(a)
    a.add_child(e)
    try:
        dag = DAG(l)
        test3 = 0
        print "Test3: FAILED"
    except AssertionError:
        test3 = 1
        print "Test3: OK"
    return alltrue(array([test1,test2,test3]))
        
    
    