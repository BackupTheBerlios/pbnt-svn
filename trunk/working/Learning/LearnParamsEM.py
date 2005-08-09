def learnParamsEM( engine, trials, iterations ):
        
        converge = True
        iter = 0
        #assume that all CPTs were initialized already.
        while not converge and iter < iterations:
                iter += 1
                for evI in range(shape(trials)[1]):
                        ev = trials[:,evI]
                        engine.evidence = ev
                        blankNodes = engine.bnet.nodes[ev == -1]
                        Q = engine.marginal(blankNodes)
                        #need to look through update ess a little more, but assume that i sample here
                        for (q,i) in zip(Q, where(ev==-1)[0]):
                                val = sample(q)
                                ev[i] = val
                        
                        #update counts of bnet
                        
                                
                        