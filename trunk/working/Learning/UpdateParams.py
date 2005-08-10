from numarray import *
import utilities


def updateParams (bnet, trials):
	counts = bnet.counts()
	for t in range(shape( trials )[1]): 
		trial = trials[:,t]
		utilities.updateCounts(bnet.nodes, counts, trial)
	
	bnet.addCounts(counts)
		

		