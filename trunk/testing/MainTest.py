import BayesNetTest
import EnumerationTest
import JunctionTreeTest
import UtilitiesTest
import SequenceGeneratorTest
import MCMCEngineTest
from numarray import *

print "starting tests"
Msuccess = MCMCEngineTest.test()
JTsuccess = JunctionTreeTest.test()
Esuccess = EnumerationTest.test()
Ssuccess = SequenceGeneratorTest.test()
Usuccess = UtilitiesTest.test()
Bsuccess = BayesNetTest.test()


if alltrue(Bsuccess) and alltrue(Esuccess) and alltrue(Usuccess) and alltrue(JTsuccess) and alltrue(Msuccess):
  print "ALL TESTS SUCCESSFUL"
else:
  print "BayesNet Failed AT: %s\n", (where(Bsuccess==0)[0])
  print "Enumeration Failed AT: %s\n", (where(Esuccess==0)[0])
  print "Utilities Failed AT: %s\n", (where(Usuccess==0)[0])
  
print "finished tests"



