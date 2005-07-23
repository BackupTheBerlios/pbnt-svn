class EliminationEngine inherits from InferenceEngine:

def marginal(X):
	vars = reverse(bnet.vars)
	e = self.evidence
	for var in vars:
		factors = factors.append(Factor(var,e))
		if isHidden(var,e):
			factors = SumOut(var,factors)

return pointwise-product(factors).normalize()


def SumOut (var, factors):
	dependent = []
	independent = []
	for factor in factors:
		if DependentFactor(var, factor):
			dependent.append(factor)
		else:
			independent.append(factor)
	pointfactors = []
	for val in var.values:
		pointfactors.append(PointwiseProduct(dependent, var, val))

	independent.append(SumFactors(pointfactors))

	return independent


#slightly different fromlisp.  
#Takes a var and a val, and reduces
# each factor in the factorList by 
#setting var to val.
def PointwiseProduct(factorList, var, val):
	#not the best way todo this, 
	#because taken fromlisp, but 
	#good for now
	vars = RemoveDuplicates(factorList[:].vars)

	dims = vars[:].size

	#create an array with the dims 
	#specified in dims
	table = array(dims)





#assumes that each factor is over 
#thesame variables and therefore 
#hasthe same dimensions.
#TODO: error checking.
def SumFactors ( factorList ):
	table = factorList[0].table
	vars = factorList[0].vars
	for factor in factorList[1:]:
		table += factor.table
	return Factor(table, vars)



Summing-Out a variable from a product of factors: move any constant factors outside the sumation add up submatrices in pointwise porduct of remaining factors

Pointwise product of factors f1 and f2:
f1(x1,...,xj,y1,...yk) * f2(y1,...,yk,z1,...,zl)
= f(x1,...,xj,y1,...,yk,z1,...,zl)
EG f1(a,b) * f2(b,c) = f(a,b,c)


