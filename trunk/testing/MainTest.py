import BayesNetTest
import EnumerationTest
import UtilitiesTest
from numarray import *

print "starting tests"
Bsuccess = BayesNetTest.test()
Esuccess = EnumerationTest.test()
Usuccess = UtilitiesTest.test()
if all(Bsuccess) and all(Esuccess) and all(Usuccess):
  print "ALL TESTS SUCCESSFUL"
else:
  print "BayesNet Failed AT: %s\n", (where(Bsuccess==0)[0])
  print "Enumeration Failed AT: %s\n", (where(Esuccess==0)[0])
  print "Utilities Failed AT: %s\n", (where(Usuccess==0)[0])
  
print "finished tests"



