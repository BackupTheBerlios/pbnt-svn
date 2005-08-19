import BayesNetTest
import EnumerationTest
import JunctionTreeTest
import UtilitiesTest
import MCMCEngineTest
from numarray import *

print "starting tests"
print "starting Junction Tree"
JTsuccess = JunctionTreeTest.test()
print "starting MCMC"
Msuccess = MCMCEngineTest.test()
print "Enumeration"
Esuccess = EnumerationTest.test()
print "SequenceGenerator"
Ssuccess = SequenceGeneratorTest.test()
print "starting Utilities"
Usuccess = UtilitiesTest.test()

if alltrue(Esuccess) and alltrue(Usuccess) and alltrue(JTsuccess) and alltrue(Msuccess):
  print "ALL TESTS SUCCESSFUL"
else:
  print "JunctionTree Failed AT: %s\n", (where(JTsuccess==0)[0])
  print "Enumeration Failed AT: %s\n", (where(Esuccess==0)[0])
  print "Utilities Failed AT: %s\n", (where(Usuccess==0)[0])
  print "MCMC Failed AT: %s\n", (where(Msuccess==0)[0])
  
print "finished tests"



