#Major Packages
from numarray import *
import numarray.ieeespecial as ieee

#Local Project Modules
from Graph import *
from Node import *
from Utilities.Utilities import *
import Utilities.GraphUtilities as GraphUtilities

"""This is the InferenceEngine module.  It defines all inference algorithms.  All of these inference algorithms are implemented as "engines", which means that they wrap around a bayes net in order to create a new inference object that can be treated abstractly.  One reason for this is that abstract inference objects can be used by other methods such as learning algorithms in the same ways regardless of which inference method is actually being used. 
"""

class InferenceEngine:
    """ This is the parent class of all inference engines.  It defines several very basic methods 
    that are used by all inference engines.
    """
    
    def __init__(self, bnet):
        self.bnet = bnet
        self.evidence = zeros(bnet.numNodes) + -1

    def init_evidence(self, evidence):
        self.evidence = evidence
        
    def change_evidence ( self, varIndex, values ):
        self.evidence[varIndex] = values
    
    def marginal(self):
        self.action()


class EnumerationEngine(InferenceEngine):
    """ Enumeration Engine uses an unoptimized fully enumerate brute force method to compute the 
    marginal of a query.  It also uses the standard constructor, init_evidence, and 
    change_evidence methods.  In this engine, we use a hack.  We have to check and see if the 
    variable is unobserved.  If it is not, then we know that the probability of that value is 
    automatically 1.  We use this hack, because in order to do it properly, a table of likelihoods
    that incorporates the evidence would have to be constructed, this is very costly.
    """

    def marginal ( self, nodes ):
        # Compute the marginal for each node in nodes
        distList = list()
        for node in nodes:
            ns = node.ns
            # Create the return distribution.
            Q = DiscreteDistribution(ns)
            if self.evidence[node.index] == -1:
                 for val in range(ns):
                     prob = self.enumerate_all(node, val)
                     Q.set_value(val, prob)
            else:
                val = self.evidence[node.index]
                Q.set_value(val, 1)
            Q.normalize()
            distList += Q
        return distList
    
    """ The following methods could be functions, but I made them private methods because they
    are functions that should only be used internally to the class.
    ADVICE: James, do you think these should remain as private methods or become function calls?
    """

    def __enumerate_all (self, node, value):
        """ We are going to iterate through all values of all non-evidence nodes. For each state
        of the evidence we sum the probability of that state by the probabilities of all 
        other states.
        """
        oldValue = self.evidence[node.index]
        # Set the value of the query node to value, since we don't want to iterate over it.
        self.change_evidence(node.index, value)
        nonEvidence = where(self.evidence == -1)[0]
        self.initialize(nonEvidence)
        # Get the probability of the initial state of all nodes.
        prob = self.probability(self.evidence)
        while self.nextState(nonEvidence):
            prob += self.probability(self.evidence)
        # Restore the state of evidence to its state at the beginning of enumerate_all.
        self.evidence[nonEvidence] = -1
        self.change_evidence(node.index, oldValue)
        return Q
    
    def __initialize(self, nonEvidence):
        self.evidence[nonEvidence] = 0
    
    def __next_state(self, nonEvidence):
        # Generate the next possible state of the evidence.
        numberOfNodes = len(nonEvidenceNodes)
        for index in nonEvidence:
            if self.evidence[index] == (self.bnet.nodes(index).nodeSize - 1):
                # If the value of the node is its max value, then reset it.
                if index == nonEvidence[numberOfNodes - 1]:
                    # If we iterated through to the last nonEvidence node, and didn't find a new 
                    # value, then we have visited every possible state.
                    return False
                else:
                    self.evidence[node] = 0
                    continue
            else:
                self.evidence[node] += 1
                break
        return True
        
    def __probability(self, state):
        # Compute the probability of the state of the bayes net given the values of state.
        Q = 1
        for i in range(len(state)):
            vals = concatenate((state[self.bnet.parentIndices(i)], state[i]))
            Q *= self.bnet.nodes(i).getValue(vals)
        return Q


class JunctionTreeEngine( InferenceEngine ):
    #for reference please read, "Belief Networks: A Procedural Guide" by Cecil Huang and Adnan Darwiche (1994)

    def __init__ (self, bnet):
        InferenceEngine.__init__(self, bnet)
        #create the moral graph
        moralGraph = MoralGraph( self.bnet )
        #triangulate the graph
        triangulatedGraph = TriangleGraph( moralGraph )
        #build a join tree and initialize it
        self.joinTree = self.BuildJoinTree(triangulatedGraph)
    
    def marginal(self, query):
        #ASSUMPTION: BuildJoinTree initializes potentials
        #do global propagation
        #for each message pass, maginalize over a X which means to find the instantiations
        #of X that are consitent with R and sum them
        #absorption identify the values of Y that are consisten with X (through sepset R)
        #and multiply each element and set Y to be that result (for pass from X to Y)
        if not self.joinTree.initialized:
            self.joinTree.reInitialize( self.bnet.nodes )
        
        self.joinTree.enterEvidence( self.evidence, self.bnet.nodes )
        self.globalPropagation()
        
        #assuming no evidence
        distributions = []
        for node in query:
            Q = DiscreteDistribution( zeros([node.nodeSize], type=Float32), node.nodeSize )
            for value in range( node.nodeSize ):
                #axis arg not needed, but nice for clarity
                Q.setValue( value, node.clique.CPT.getValue( [value], axes=[node.clique.nodes.index(node)] ).sum(), axes=[0] )
            Q.normalise()
            distributions.append( Q )
        
        return distributions
        
        
    def globalPropagation( self ):
        self.joinTree.initialized = False
        #arbitrarily pick a cluster
        startCluster = self.joinTree.nodes[0]
        
        GraphUtilities.unmarkAllNodes( self.joinTree )
        #we use 0 to denote that there was no prevCluster and therefore no potential or mu
        self.collectEvidence( 0, startCluster, 0, True )
        GraphUtilities.unmarkAllNodes( self.joinTree )
        self.distributeEvidence( startCluster )
    
    def collectEvidence( self, prevCluster, currentCluster, sepset, isStart ):
        currentCluster.visited = 1
        for (neighbor, sep) in zip(currentCluster.neighbors, currentCluster.sepsets):
            if not neighbor.visited:
                self.collectEvidence( currentCluster, neighbor, sep, 0 )
            
        if not isStart:
            self.passMessage( currentCluster, prevCluster, sepset )
    
    def distributeEvidence( self, cluster ):
        cluster.visited = 1
        for (neighbor, sep) in zip( cluster.neighbors, cluster.sepsets ):
            if not neighbor.visited:
                self.passMessage( cluster, neighbor, sep )
                self.distributeEvidence( neighbor )
    
    def passMessage( self, fromCluster, toCluster, sepset ):
        #projection
        oldSepsetPotential = self.project( fromCluster, sepset ) 
        #absorption
        self.absorb( toCluster, sepset, oldSepsetPotential )
    
    def project( self, cluster, sepset ):
        oldSepsetPotential = copy.deepcopy( sepset.potential )
        #not using mu anymore but not ready to delete yet
        mu = sepset.mu
        clusterAxes = sepset.cliqueAxes( cluster )
        sepsetAxis = sepset.axis
        for index in mu:
            #get the relevant entries out of the cluster potential
            values = array([cluster.CPT.getValue( index, clusterAxes )])
            sepset.potential.setValue( index, values.sum(), axes=sepsetAxis )
        return oldSepsetPotential
                
    def absorb( self, cluster, sepset, oldPotential ):
        mu = sepset.mu
        sepsetAxis = sepset.axis
        clusterAxes = sepset.cliqueAxes( cluster )
        zeroMask = oldPotential.CPT == 0
        oldPotential.CPT = sepset.potential.CPT / oldPotential.CPT
        oldPotential.CPT[zeroMask] = 0 
        #saxesToIter = [axis for axis in range(cluster.CPT.nDims) if not axis in clusterAxes]
        #multiply and set potential, assumes that there is only one axis of difference between
        #sepset and cluster
        for index in mu:
            sepsetValue = oldPotential.getValue( index, sepsetAxis )
            clusterValues = cluster.CPT.getValue( index, clusterAxes )
            newValues = clusterValues * sepsetValue
            cluster.CPT.setValue( index, newValues, clusterAxes )
            #if len( axesToIter ) > 0:
                #dimsToIter = array(cluster.CPT.dims)[axesToIter]
                #indices = generateArrayIndex( dimsToIter, axesToIter, index, clusterAxes )
                ##flatindices = convertIndex( indices )
                #cluster.CPT.setValue( indices, newValues, clusterAxes )
            #else:
                ##flatindex = sum( index * array([cluster.indexWeights[cA] for cA in clusterAxes]) )
                #cluster.CPT.setValue( index, newValues, clusterAxes )
            
    

    def BuildJoinTree (self, triangulatedGraph):
        
        #build the join tree from the cliques in triangulatedGraph
        cliques = triangulatedGraph.cliques
        forest = [JoinTree( clique ) for clique in cliques]
        sepsetHeap = PriorityQueue()
        for i in range(len( cliques ) - 1):
            for clique in cliques[i+1:]:
                sepset = Sepset( cliques[i], clique )
                sepsetHeap.insert( sepset )
        
        for n in range(len( forest ) - 1):
            #insert sepsets into JoinTree
            while sepsetHeap.hasNext():
                sepset = sepsetHeap.next()
                joinTreeX = GraphUtilities.getTree( forest, sepset.cliqueX )
                joinTreeY = GraphUtilities.getTree( forest, sepset.cliqueY )
                if joinTreeX != joinTreeY:
                    joinTreeX.merge( sepset, joinTreeY )
                    forest.remove( joinTreeY )
                    break
            
        for tree in forest:
            tree.initCliquePotentials( self.bnet.nodes )
        
        #find out if we are dealing with a forest, if so return as list, otherwise return as individual tree
        if len( forest ) > 1:
            return forest
        else:
            return forest[0]
    


class JunctionTreeDBNEngine(JunctionTreeEngine):
    #this is named DBN, but really it only works for HMMs for now.
    
    def __init__(self, DBN):
        InferenceEngine.__init__(DBN)
        moral = MoralDBNGraph(DBN)
        #triangulate the graph
        triangulatedGraph = TriangleGraph( moralGraph )
        #build a join tree and initialize it
        self.joinTree = self.BuildJoinTree(triangulatedGraph)
        
