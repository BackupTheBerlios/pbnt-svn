def update_params (bnet, trials):
#destructive parameter update, 
#basically set the bnet table to be the 
#params that are specified in trials

#assumes that bnet initializes all of its 
#distributions to have a nonzero entries
	for j in [0:size(trials,2)-1]:
		ev = take(trials,j)
		for i in [1:bnet.numberOfNodes()]:
			indices=  bnet.parentIndices(i)
			indices = [i] + indices
			vals = take(state,indices)

			bnet.var(i).updateValues(vals)

	for var in bnet.vars():
		var.normalize()
		

			 	
