from utilities import *
from numarray import *
#tests the various utility functions

def test():
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
    
  
  return array([test1, test2])