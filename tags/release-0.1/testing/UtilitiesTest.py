from numarray import *
from Utilities import *


def test():
  #test myFloatEQ (which is now deprecated, use allclose from numarray

  test1 = 1
  if myFloatEQ(0.055000000000000014, 0.0550):
    print "Test 1: OK\n"
  else:
    test1 = 0
    print "Test 1: FAILED\n"
  
  
  test2 = 1
  if not myFloatEQ(0.055000000000000014, 0.0551):
    print "Test 2: OK\n"
  else:
    test2 = 0
    print "Test 2: FAILED\n"
  
  #test unique
  a = array([1,2,3])
  b = array([4,5,6])
  c = array([1,3,2])
  d = array([5,6,10,3,1,3,7,7])

  test3 = 1
  if alltrue(unique( (a, c) ) == a):
    print "\tTest3A: OK\n"
  else:
    test3 = 0
    print "\tTest3A: FAILED\n"
    
  if alltrue(unique( (a, b) ) == array([1,2,3,4,5,6])):
    print "\tTest3B: OK\n"
  else:
    test3 = 0
    print "\tTest3B: FAILED\n"
  
  if alltrue(unique( (a, d) ) == array([1,2,3,5,6,10,7])):
    print "\tTest3C: OK\n"
  else:
    test3 = 0
    print "\tTest3C: FAILED\n"

  if test3:
    print "Test 3: OK\n"
  else:
    print "Test 3: FAILED\n"
    
    
  
  #test addToPriorityQueue
  test4 = 1
  a = [3,2,1]
  a = addToPriorityQueue( a, 1.5 )
  if a == [3,2,1.5,1]:
    print "\tTest 4A: OK\n"
  else:
    test4 = 0
    print "\tTest 4A: FAILED\n"
  
  a = addToPriorityQueue( a, 0 )
  if a == [3,2,1.5,1,0]:
    print "\tTest 4B: OK\n"
  else:
    test4 = 0
    print "\tTest 4B: FAILED\n"  
  
  a = addToPriorityQueue( a, 4 )
  if a == [4,3,2,1.5,1,0]:
    print "\tTest 4C: OK\n"
  else:
    test4 = 0
    print "\tTest 4C: FAILED\n"
  
  if test4:
    print "Test 4: OK\n"
  else:
    print "Test 4: FAILED\n"
  
  return array([test1, test2, test3, test4])