def learnParamsEM( engine, trials, iterations ):
        
        converge = True
        iter = 0
        #assume that all CPTs were initialized already.
        while not converge and iter < iterations:
                
                for evI in range(shape(trials)[1]):
                        ev = trials[:,evI]
                        engine.evidence = ev
                        blankDist = engine.marginal(engine.bnet.nodes[ev == -1])
                        