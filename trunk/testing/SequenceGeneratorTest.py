import SequenceGenerator
from numarray import *

def test():
        sequence = SequenceGenerator.SequenceGenerator( [2,2] )
        
        seqs = []
        for seq in sequence:
                print seq
                seqs.append( seq.copy() )
        
        test1 = 1
        if all( seqs[0] == array([0,0]) ):
                print "Test 1: OK\n"
        else:
                test1 = 0
                print "Test 1: FAILED\n"
        
        
        test2 = 1
        if all( seqs[1] == array([1,0]) ):
                print "Test 2: OK\n"
        else:
                test2 = 0
                print "Test 2: FAILED\n"
        
        test3 = 1
        if all( seqs[2] == array([0,1]) ):
                print "Test 3: OK\n"
        else:
                test3 = 0
                print "Test 3: FAILED\n"
        
        test4 = 1
        if all( seqs[3] == array([1,1]) ):
                print "Test 4: OK\n"
        else:
                test4 = 0
                print "Test 4: FAILED\n"
        
        return array([test1,test2,test3,test4])