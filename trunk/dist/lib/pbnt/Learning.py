from numarray import *
import utilities




def updateParams (bnet, trials):
    counts = bnet.counts()
    for t in range(shape( trials )[1]): 
        trial = trials[:,t]
        utilities.updateCounts(bnet.nodes, counts, trial)
    bnet.add_counts(counts)


#We are going to start with a very simple but poor approach.  We are going to use the engine
#to compute the marginal distribution over the unobserved nodes.  Then we are going to sample 
#from this distribution, fill in the missing value of the evidence, and treat it as a fully observed
#evidence case.

def learnParamsEM( engine, trials, iterations ):
    #Perform "iterations" EM steps
    for iter in range(iterations):
        counts = engine.bnet.counts()
        #For each iteration we want to iterate through all of the evidence cases
        for evI in range(shape(trials)[1]):
            ev = trials[:,evI]
            #find the unobserved nodes
            blankNodes = engine.bnet.nodes[ev == -1]
            if len(blankNodes) > 0:
                #if there are unobserved nodes compute
                #the marginal distribution of those nodes given the observed 
                #nodes
                engine.evidence = ev
                Q = engine.marginal(blankNodes)
                for (q,i) in zip(Q, where(ev==-1)[0]):
                    #for each unobserved node sample the value
                    #given the marginal distribution
                    val = sample(q)
                    ev[i] = val
            
            #update the counts matrix
            utilities.updateCounts(engine.bnet.nodes, counts, ev)
            
            #reset the evidence to -1 so that the 
            #next iteration is unaffected by this iteration
            ev[blankNodes] = -1
        
        #now update the parameters of the bayes net
        engine.bnet.addCounts(counts)
        