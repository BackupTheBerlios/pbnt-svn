def update_params (bnet, trials):
#creates a table of counts for all of the variables assumes complete data. 
#after generating table updates the distributions of each variable
	for t in range(shape( trials )[1]): 
		trial = trials[:,t]
		for node in bnet.nodes:
			values = trial[concatenate((node.parentIndex, array([node.index])))]
			currentValue = node.CPT.getValue( values )
			currentValue += 1
			node.CPT.setValue( values, currentValue )
	
	for node in bnet.nodes:
		node.CPT.normalise()
		


			 	
