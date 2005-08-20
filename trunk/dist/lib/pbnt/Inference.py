#Major Packages
from numarray import *
import numarray.ieeespecial as ieee
import numarray.random_array as ra

#Local Project Modules
from Graph import *
from Node import *
from Distribution import *
from Utilities import *
import GraphUtilities

"""This is the InferenceEngine module.  It defines all inference algorithms.  All of these inference algorithms are implemented as "engines", which means that they wrap around a bayes net in order to create a new inference object that can be treated abstractly.  One reason for this is that abstract inference objects can be used by other methods such as learning algorithms in the same ways regardless of which inference method is actually being used. 
"""

class InferenceEngine:
    """ This is the parent class of all inference engines.  It defines several very basic methods that are used by all inference engines.
    """
    
    def __init__(self, bnet):
        self.bnet = bnet
        self.evidence = zeros(bnet.numNodes) + -1

    def init_evidence(self, evidence):
        self.evidence = evidence
        
    def change_evidence (self, varIndex, values):
        self.evidence[varIndex] = values
    
    def marginal(self):
        self.action()


class EnumerationEngine(InferenceEngine):
    """ Enumeration Engine uses an unoptimized fully enumerate brute force method to compute the marginal of a query.  It also uses the standard constructor, init_evidence, and change_evidence methods.  In this engine, we use a hack.  We have to check and see if the variable is unobserved.  If it is not, then we know that the probability of that value is automatically 1.  We use this hack, because in order to do it properly, a table of likelihoods that incorporates the evidence would have to be constructed, this is very costly.
    """

    def marginal(self, nodes):
        if not isinstance(nodes, types.ListType):
            nodes = [nodes]
        # Compute the marginal for each node in nodes
        distList = list()
        for node in nodes:
            ns = node.size()
            # Create the return distribution.
            Q = DiscreteDistribution(ns)
            if self.evidence[node.index] == -1:
                 for val in range(ns):
                     prob = self.__enumerate_all(node, val)
                     index = Q.generate_index([val], range(Q.nDims))
                     Q[index] = prob
            else:
                val = self.evidence[node.index]
                index = Q.generate_index(val, range(Q.nDims))
                Q[index] = 1
            Q.normalize()
            distList.append(Q)
        return distList
    
    """ The following methods could be functions, but I made them private methods because the are functions that should only be used internally to the class. ADVICE: James, do you think these should remain as private methods or become function calls?
    """

    def __enumerate_all(self, node, value):
        """ We are going to iterate through all values of all non-evidence nodes. For each state of the evidence we sum the probability of that state by the probabilities of all other states.
        """
        oldValue = self.evidence[node.index]
        # Set the value of the query node to value, since we don't want to iterate over it.
        self.change_evidence(node.index, value)
        nonEvidence = where(self.evidence == -1)[0]
        self.__initialize(nonEvidence)
        # Get the probability of the initial state of all nodes.
        prob = self.__probability(self.evidence)
        while self.__next_state(nonEvidence):
            prob += self.__probability(self.evidence)
        # Restore the state of evidence to its state at the beginning of enumerate_all.
        self.evidence[nonEvidence] = -1
        self.change_evidence(node.index, oldValue)
        return prob
    
    def __initialize(self, nonEvidence):
        self.evidence[nonEvidence] = 0
    
    def __next_state(self, nonEvidence):
        # Generate the next possible state of the evidence.
        numberOfNodes = len(nonEvidence)
        for index in nonEvidence:
            if self.evidence[index] == (self.bnet.nodes[index].size() - 1):
                # If the value of the node is its max value, then reset it.
                if index == nonEvidence[numberOfNodes - 1]:
                    # If we iterated through to the last nonEvidence node, and didn't find a new 
                    # value, then we have visited every possible state.
                    return False
                else:
                    self.evidence[index] = 0
                    continue
            else:
                self.evidence[index] += 1
                break
        return True
        
    def __probability(self, state):
        # Compute the probability of the state of the bayes net given the values of state.
        Q = 1
        for i in range(len(state)):
            node = self.bnet.nodes[i]
            dist = node.dist
            vals = state[node.evidence_index()]
            # Generate a slice object to index into dist using vals.
            index = dist.generate_index(vals, range(dist.nDims))
            Q *= node.dist[index]
        return Q

class MCMCEngine( InferenceEngine ):
        #implemented as described in Russell and Norvig
        #X is a list of variables
        #N is thenumber of samples
        def marginal ( self, X, N ):
            flipped = 0
            Nx = [DiscreteDistribution(x.size()) for x in X]
            queryIndex = array([x.index for x in X])
            state = self.evidence.copy()
            nonEvMask = state == -1
            nonEv = obj.array(self.bnet.nodes)[nonEvMask]
            randMax = array([node.size() for node in nonEv])
            #ASSUMPTION: zero is the minimum value
            randMin = zeros([len( nonEv )])
            #initialize nonEvidence variables to random values
            state[nonEvMask] = ra.randint( randMin, randMax )
            #FOR DEBUGGING ONLY
            valuesList = []
            for i in range( N ):
                valuesList += [state[3]]
                #record the value of all of the query variables
                if i > 100:
                    for (q, dist) in zip(queryIndex, Nx):
                        dist.CPT[state[q]] += 1
                        for node in nonEv:
                            val = self.sampleValueGivenMB(node, state)
                            #change the state to reflect new value of given variable
                            if not state[node.index] == val:
                                state[node.index] = val
                                flipped += 1               
            for i in range(len( Nx )):
                Nx[i].normalise()
            return Nx
                                

        def sampleValueGivenMB( self, node, state ):
                #init to be the prob dist of node given parents
                parents = node.parents
                parentsI = array([p.index for p in parents])
                #ASSUMPTION: node is arranged by parents
                MBval = node.CPT.getValue( state[parentsI], axes=range( node.CPT.nDims - 1 ) )
                children = node.children
                #want to save state
                oldVal = state[node.index]
                #OPTIMIZE: could vectorize this code
                for value in range(node.size()):
                        state[node.index] = value
                        for child in children:
                                childPsI = [p.index for p in child.parents]
                                parentVals = state[childPsI]
                                childVal = state[child.index]
                                indices = concatenate((parentVals, childVal))
                                MBval[value] *= child.CPT.getValue(indices)
                
                state[node.index] = oldVal
                #FIX THIS: better representation of distributions
                #normalize MBval
                MBval /= MBval.sum()
                
                val = util.sample(MBval)
                return val


class JunctionTreeEngine(InferenceEngine):
    """ This implementation of the Junction Tree inference algorithm comes from "Belief Networks: A Procedural Guide" By Cecil Huang an Adnan Darwiche (1996).  See also Kevin Murhpy's PhD Dissertation.  Roughly this algorithm decomposes the given bayes net to a moral graph, triangulates the moral graph, and collects it into cliques and joins the cliques into a join tree.  The marginal is then computed from the constructed join tree.
    """

    def __init__ (self, bnet):
        # Still use the built in constructor, but then add on to it
        InferenceEngine.__init__(self, bnet)
        # Create the moral graph
        moralGraph = MoralGraph(self.bnet)
        # Triangulate the graph
        triangulatedGraph = TriangleGraph( moralGraph )
        # Build a join tree and initialize it.
        self.joinTree = self.build_join_tree(triangulatedGraph)
    
    #def change_evidence(self, nodes, values):
        #""" Override parent's method because in a junction tree we have to perform an update or a retraction based on the changes to the evidence.
        #"""
        ## 0 = no change, 1 = update, 2 = retract
        #isChange = 0
        #changedNodes = []
        #for (node, value) in zip(nodes, values):
            ## Make sure node has actually changed
            #if not self.evidence[node.index] == value:
                #changedNodes += node
                ## Check if node is retracted
                #if not self.evidence[node.index] == -1:
                    #isChange = 2
                    #break
                #else:
                    #isChange = 1
        
        #if isChange == 1:
            ## Just to avoid import errors
            #assert(1 == 1)
            
            ## Do a global update
            #for node in changedNodes:
                ## Just to avoid import errors
                #assert(1 == 1)
            
                ## Update potential X and its likelihood with the new observation
                ## Then do global propagation (if only 1 cluster affected only have 
                ## to distribute evidence.
        #elif isChange == 2:
            ## Do a global retraction: Encode the new likelihoods (and do observation entry), 
            ## Reinitialize the join tree, do a Global propagation.
            
            ## Just to avoid import errors
            #assert(1 == 1)
                
    def marginal(self, query):
        # DELETE: When change_evidence is completed delete this.
        if not self.joinTree.initialized:
            self.joinTree.re_initialize(self.bnet.nodes)
        
        self.joinTree.enter_evidence(self.evidence, self.bnet.nodes)
        self.global_propagation()
        # DELETE: End delete here
        
        distributions = []
        for node in query:
            Q = DiscreteDistribution(node.size())
            for value in range(node.size()):
                potential = node.clique.potential
                index = potential.generate_index([value], [node.clique.nodes.index(node)])
                Q[value] = potential[index].sum()
            Q.normalize()
            distributions.append(Q)
        return distributions
        
        
    def global_propagation(self):
        self.joinTree.initialized = False
        # Arbitrarily pick a clique to be the root node, could be OPTIMIZED
        startClique = self.joinTree.nodes[0]
        GraphUtilities.unmark_all_nodes(self.joinTree)
        # We use 0 to denote that there was no prevCluster
        self.collect_evidence(0, startClique, 0, True)
        GraphUtilities.unmark_all_nodes(self.joinTree)
        self.distribute_evidence(startClique)
    
    def collect_evidence(self, prevClique, currentClique, sepset, isStart):
        # In this stage we send messages from the outer nodes toward a root node.
        currentClique.visited = 1
        for (neighbor, sep) in zip(currentClique.neighbors, currentClique.sepsets):
            # Do a DFS search of the tree, only visiting unvisited nodes
            if not neighbor.visited:
                self.collect_evidence(currentClique, neighbor, sep, 0)
        if not isStart:
            # After we have found the leaf (or iterated over all neighbors) send a message
            # back toward the root.
            self.pass_message(currentClique, prevClique, sepset)
    
    def distribute_evidence(self, clique):
        # Send messages from root node out toward leaf nodes
        clique.visited = 1
        for (neighbor, sep) in zip(clique.neighbors, clique.sepsets):
            # Perform DFS passing messages as we go from one node to the next
            if not neighbor.visited:
                self.pass_message(clique, neighbor, sep)
                self.distribute_evidence(neighbor)
    
    def pass_message(self, fromClique, toClique, sepset):
        # Project the fromCluster onto the sepset, oldSepsetPotential is the sepset's potential
        # before it is affected by the internals of project
        oldSepsetPotential = self.project(fromClique, sepset) 
        # Absorb the sepset into the toCluster
        self.absorb(toClique, sepset, oldSepsetPotential)
    
    def project(self, clique, sepset):
        # project marginalizes the clique given the variables in the sepset
        oldSepsetPotential = copy.deepcopy(sepset.potential)
        # This list of axes orders the standard range(sepset.potential.nDims) so that it references the clique.
        cliqueAxes = sepset.clique_axes(clique)
        # This could be optimized by finding a better way index clique with all of the seqs at the same time
        # and then summing over those possible values and assigning the answer to the sepset potential.
        sequence = SequenceGenerator(sepset.potential.dims)
        for seq in sequence:
            index = clique.potential.generate_index(seq, cliqueAxes)
            seqIndex = sepset.potential.generate_index(seq, range(sepset.potential.nDims))
            sepset.potential[seqIndex] = clique.potential[index].sum()
        return oldSepsetPotential
                
    def absorb(self, clique, sepset, oldPotential):
        # absorb divides sepset.potential (the newly affected potential) by oldPotential (the one 
        # unaffected by project).  Then multiply the result by the clique's potential.
        # The axes of clique that correspond to the variables in sepset.
        cliqueAxes = sepset.clique_axes(clique)
        # Wherever oldPotential == 0 we are guaranteed to have sepset.potential == 0. So to avoid
        # divide by 0 warnings we set these places to 1.
        oldPotential[oldPotential[:] == 0] = 1
        # Division of the new and old potentials
        sepset.potential[:] /= oldPotential[:]
        for seq in SequenceGenerator(sepset.potential.dims):
            index = clique.potential.generate_index(seq, cliqueAxes)
            seqIndex = sepset.potential.generate_index(seq, range(sepset.potential.nDims))
            clique.potential[index] *= sepset.potential[seqIndex]

    def build_join_tree (self, triangulatedGraph):
        # The Triangulated Graph is really a graph of cliques.
        cliques = triangulatedGraph.cliques
        # We start by creating a forest of trees, one for each clique.
        forest = [JoinTree(clique) for clique in cliques]
        sepsetHeap = PriorityQueue()
        # Create sepsets by matching each clique with every other clique.
        # We need to generate a unique id for each sepset.
        id = 0
        for i in range(len(cliques) - 1):
            for clique in cliques[i+1:]:
                sepset = Sepset(id, cliques[i], clique)
                id += 1
                sepsetHeap.insert(sepset)
        
        # Join n - 1 sepsets together forming (hopefully) a single tree.
        for n in range(len(forest) - 1):
            while sepsetHeap.hasNext():
                # Get the sepset with the maximum mass breaking ties by
                # choosing the sepset with the smallest cost.
                sepset = sepsetHeap.next()
                # Find out which tree each clique is from
                joinTreeX = GraphUtilities.getTree(forest, sepset.cliqueX)
                joinTreeY = GraphUtilities.getTree(forest, sepset.cliqueY)
                if not joinTreeX == joinTreeY:
                    # If the cliques are on different trees, then join to make a larger one.
                    joinTreeX.merge(sepset, joinTreeY)
                    forest.remove(joinTreeY)
                    break
                
        for tree in forest:
            tree.init_clique_potentials(self.bnet.nodes)
        
        # We return the forest here, but in reality we are only set to 
        # compute marginals on a single tree, not a forest of trees.
        if len( forest ) > 1:
            return forest
        else:
            return forest[0]
    

class JunctionTreeDBNEngine(JunctionTreeEngine):
    """ JunctionTreeDBNEngine is the JunctionTreeEngine for dynamic networks.  It is far from done.  This is more of a place holder as of right now.
    """
    
    def __init__(self, DBN):
        InferenceEngine.__init__(DBN)
        moral = MoralDBNGraph(DBN)
        #triangulate the graph
        triangulatedGraph = TriangleGraph( moralGraph )
        #build a join tree and initialize it
        self.joinTree = self.BuildJoinTree(triangulatedGraph)
        
