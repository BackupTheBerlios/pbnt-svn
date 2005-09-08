# PBNT: Python Bayes Network Toolbox
#
# Copyright (c) 2005, Elliot Cohen
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
# * The name "Elliot Cohen" may not be used to endorse or promote
#   products derived from this software without specific prior written
#   permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from numarray import *
from Utilities import Utilities

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
        
