# Major packages
from numarray import *

#Local modules
from Node import *
from Graph import *
from Inference import *
import ExampleModels as EX

""" This file is a set of unit tests.  They are all written as separate functions that return true or false.
"""

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
        