class MCMCEngine inherits from InferenceEngine:

	#X is a list of variables
	#N is thenumber of samples
	def marginal ( X, N ):
		#create a list of arrays 
		#where each arrary is 
		#ns of the corresonding 
		#query variable
		Nx = [for x in X zeros(x.ns)]
		state = self.evidence()
		nonEv = setdiff(list(0:self.bnet().numVars()), nonzeros(self.evidence()))

#could optimize this to be the values 
#of x given their MB if it is specified, 
#basically couldhave a better guess.

		#initialize nonEV variables so that state is complete
		for i in nonEv:
			take(state,i) = round(rand(1,self.bnet().vars()[i].ns))

#indexes for indexinginto Nx
		rowIndex = array(1:size(Nx,1))

		for 1 to N:
			for i in [1:length(nonEv)]:
#memoize MB calc at some point

				val = valueGivenMB(nonEv[i], state)
				take(state,nonEv[i]) = val
 
				take(Nx[i], val) += 1

		return normalize(Nx)


#sample the value of the given 
#variable given the values of its 
#markov blanket, might need to 
#normalize return value
def valueGivenMB ( varIndex , state):
	MBval = 1
	selfChildren = [varIndex] + self.bnet().children(varIndex)
	for varI in selfChildren:
		MBval *= self.bnet().vars()[varI].prob(take(state, self.bnet().parents(varI)))

	return MBval


