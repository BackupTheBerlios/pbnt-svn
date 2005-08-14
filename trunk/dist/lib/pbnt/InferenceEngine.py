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


class JunctionTreeEngine(InferenceEngine):
    """ This implementation of the Junction Tree inference algorithm comes from "Belief Networks: 
    A Procedural Guide" By Cecil Huang an Adnan Darwiche (1996).  See also Kevin Murhpy's PhD 
    Dissertation.  Roughly this algorithm decomposes the given bayes net to a moral graph, 
    triangulates the moral graph, and collects it into cliques and joins the cliques into a join 
    tree.  The marginal is then computed from the constructed join tree.
    """

    def __init__ (self, bnet):
        # Still use the built in constructor, but then add on to it
        InferenceEngine.__init__(self, bnet)
        # Create the moral graph
        moralGraph = MoralGraph(self.bnet)
        # Triangulate the graph
        triangulatedGraph = TriangleGraph( moralGraph )
        # Build a join tree and initialize it.
        self.joinTree = self.BuildJoinTree(triangulatedGraph)
    
    def change_evidence(self, nodes, values):
        """ Override parent's method because in a junction tree we have to perform an update or a 
        retraction based on the changes to the evidence.
        """
        # 0 = no change, 1 = update, 2 = retract
        isChange = 0
        changedNodes = []
        for (node, value) in zip(nodes, values):
            # Make sure node has actually changed
            if not self.evidence[node.index] == value:
                changedNodes += node
                # Check if node is retracted
                if not self.evidence[node.index] == -1:
                    isChange = 2
                    break
                else:
                    isChange = 1
        
        if isChange == 1:
            # Do a global update
            for node in changedNodes:
                # Update potential X and its likelihood with the new observation
                # Then do global propagation (if only 1 cluster affected only have 
                # to distribute evidence.
        elif isChange == 2:
            # Do a global retraction: Encode the new likelihoods (and do observation entry), 
            # Reinitialize the join tree, do a Global propagation.
                
    def marginal(self, query):
        # DELETE: When change_evidence is completed delete this.
        if not self.joinTree.initialized:
            self.joinTree.re_initialize(self.bnet.nodes)
        
        self.joinTree.enter_evidence(self.evidence, self.bnet.nodes)
        self.global_propagation()
        # DELETE: End delete here
        
        distributions = []
        for node in query:
            Q = DiscreteDistribution(zeros([node.nodeSize], type=Float32), node.nodeSize)
            for value in range(node.nodeSize):
                #axis arg not needed, but nice for clarity
                prob = node.clique.CPT.getValue([value], axes=[node.clique.nodes.index(node)])
                Q.setValue(value, prob.sum())
            Q.normalize()
            distributions.append(Q)
        return distributions
        
        
    def global_propagation(self):
        self.joinTree.initialized = False
        # Arbitrarily pick a cluster to be the root node, could be OPTIMIZED
        startCluster = self.joinTree.nodes[0]
        GraphUtilities.unmark_all_nodes(self.joinTree)
        # We use 0 to denote that there was no prevCluster
        self.collect_evidence(0, startCluster, 0, True)
        GraphUtilities.unmark_all_nodes(self.joinTree)
        self.distribute_evidence(startCluster)
    
    def collect_evidence(self, prevCluster, currentCluster, sepset, isStart):
        # In this stage we send messages from the outer nodes toward a root node.
        currentCluster.visited = 1
        for (neighbor, sep) in zip(currentCluster.neighbors, currentCluster.sepsets):
            # Do a DFS search of the tree, only visiting unvisited nodes
            if not neighbor.visited:
                self.collect_evidence(currentCluster, neighbor, sep, 0)
        if not isStart:
            # After we have found the leaf (or iterated over all neighbors) send a message
            # back toward the root.
            self.pass_message(currentCluster, prevCluster, sepset)
    
    def distribute_evidence(self, cluster):
        # Send messages from root node out toward leaf nodes
        cluster.visited = 1
        for (neighbor, sep) in zip(cluster.neighbors, cluster.sepsets):
            # Perform DFS passing messages as we go from one node to the next
            if not neighbor.visited:
                self.pass_message(cluster, neighbor, sep)
                self.distribute_evidence(neighbor)
    
    def pass_message(self, fromCluster, toCluster, sepset):
        # Project the fromCluster onto the sepset, oldSepsetPotential is the sepset's potential
        # before it is affected by the internals of project
        oldSepsetPotential = self.project(fromCluster, sepset) 
        # Absorb the sepset into the toCluster
        self.absorb( toCluster, sepset, oldSepsetPotential )
    
    def project(self, cluster, sepset):
        # Marginalize the cluster given the variables in the sepset
        oldSepsetPotential = copy.deepcopy(sepset.potential)
        # mu defines all of the indices within sepset, we use clusterAxes and sepsetAxes
        # to facilitate translation between these two domains.
        # OPTIMIZE: would be optimal to have mu iterate over the smaller of the two: num 
        # variables in sepset vs variables in cluster but not in sepset
        mu = sepset.mu
        # The axes within cluster that refer to the variables in sepset
        clusterAxes = sepset.clique_axes(cluster)
        # The sepset axes in the proper order to refer to its variables within the cluster
        sepsetAxes = sepset.axis
        for index in mu:
            # Array of values that correspond to a : over the dimensions of 
            # cluster that are not in sepset.
            values = cluster.CPT.getValue(index, clusterAxes)
            # Sum the values, because the multiple values in cluster correspond to a single place
            # in sepset.
            sepset.potential.setValue(index, values.sum(), axes=sepsetAxes)
        # We change the internal potential, but still need access to the old one, so return it.
        return oldSepsetPotential
                
    def absorb(self, cluster, sepset, oldPotential):
        # Divide sepset.potential (the newly affected potential) by oldPotential (the one 
        # unaffected by project).  Then multiply the result by the cluster's potential.
        mu = sepset.mu
        # The sepset axes in the order that corresponds to cluster.
        sepsetAxes = sepset.axis
        # The axes of cluster that correspond to the variables in sepset.
        clusterAxes = sepset.cliqueAxes( cluster )
        # This will set all values of the cluster potential to 0 that are not consistent with 
        # the evidence.
        zeroMask = oldPotential.CPT == 0
        # Division of the new and old potentials
        oldPotential.CPT = sepset.potential.CPT / oldPotential.CPT
        # Get rid of inconsistent values.
        oldPotential.CPT[zeroMask] = 0 
        for index in mu:
            # Use mu to identify the elements of each potential 
            # that should be multiplied together.
            sepsetValue = oldPotential.getValue( index, sepsetAxes )
            clusterValues = cluster.CPT.getValue( index, clusterAxes )
            newValues = clusterValues * sepsetValue
            cluster.CPT.setValue( index, newValues, clusterAxes )    


    def BuildJoinTree (self, triangulatedGraph):
        # The Triangulated Graph is really a graph of cliques.
        cliques = triangulatedGraph.cliques
        # We start by creating a forest of trees, one for each clique.
        forest = [JoinTree(clique) for clique in cliques]
        sepsetHeap = PriorityQueue()
        # Create sepsets by matching each clique with every other clique.
        for i in range(len(cliques) - 1):
            for clique in cliques[i+1:]:
                sepset = Sepset( cliques[i], clique )
                sepsetHeap.insert( sepset )
        
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
            tree.initCliquePotentials(self.bnet.nodes)
        
        # We return the forest here, but in reality we are only set to 
        # compute marginals on a single tree, not a forest of trees.
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
        
