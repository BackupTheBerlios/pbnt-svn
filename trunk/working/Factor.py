class Factor:

	def __init__(self, var, evidence):


Sampling given MB:

P(xi|MB(Xi)) = P(xi|parents(Xi))PI Zj in set Children(Xi) P(zj|parents(Zj))

MCMC (X,e,bn,N) returns anestimate of P(X|e)

Local vars: N[X], a vecotr of counts over X, initially zero
Z, the nonevidence variables in bn
X, the current state of the network, initially copied from e

Initialize x with randomvalues for vars in Y
For j=1 to N do
For each Zi in Z do
Sample the value of Zi in x from P(Zi|mb(Zi)) given the values of MB(Zi) in x
N[x] = N[x]+1 where x is the value of X in x(b)

Return normalize(N[X])
