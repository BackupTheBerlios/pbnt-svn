# Miscellaneous utility functions for use with the rest of the BayesNet Package


#Checks if a and b are equal within a fraction of error.  
#The error is that normally introduced by the imprecision of Floating point numbers
def myFloatEQ ( a , b ):
  
  bHigh = b + 0.000000000100000000
  bLow = b - 0.000000000010000000
  
  if a < bHigh and a > bLow:
    return True
  
  return False
  

