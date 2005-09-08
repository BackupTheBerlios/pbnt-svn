import EnumerationTest
import JunctionTreeTest
import MCMCEngineTest
from numarray import *

print "starting tests"
print "Enumeration"
Esuccess = EnumerationTest.test()
print "starting Junction Tree"
JTsuccess = JunctionTreeTest.test()
print "starting MCMC"
Msuccess = MCMCEngineTest.test()

if alltrue(Esuccess) and alltrue(JTsuccess) and alltrue(Msuccess):
    print "ALL TESTS SUCCESSFUL"
else:
    print "JunctionTree Failed AT: %s\n", (where(JTsuccess==0)[0])
    print "Enumeration Failed AT: %s\n", (where(Esuccess==0)[0])
    print "MCMC Failed AT: %s\n", (where(Msuccess==0)[0])
    
print "finished tests"



