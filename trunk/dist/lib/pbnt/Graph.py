from numarray import *
import Utilities.GraphUtilities as Utilities
import Utilities.Utilities as Utilities
from ClusterBinaryHeap import *
from Clique import *

try: set
except NameError:
    import sets
    set = sets.Set

class Graph:
    """ Graph is the parent of all other graph classes.  It defines a very basic undirected graph class.  It essentially is just a list of nodes, and it is the nodes that maintain their own lists of parents and children.
    """
    
    def __init__(self, nodes):
        self.nodes = nodes
        # Only used for internal membership tests, so make it private
        self.__nodeset_ = set(nodes)
        
    def add_node(self, node):
        # Check if it is a list of nodes or a single node (arrays are also type=ListType).
        if isinstance(node, types.ListType):
            for n in node:
                self.nodes.append(n)
                self.__nodeset_.add(n)
        else:
            self.nodes.append(node)
            self.__nodeset_.add(node)
        
    def member_of(self, node):
        return node in self.__nodeset_
    
    def contains(self, nodes):
        return self.__nodeset_.issuperset(nodes)
    
    def connect_nodes(node1, node2):
        node1.add_neighbor(node2)
        node2.add_neighbor(node1)
   
   
class DAG(Graph):
    """ Child of Graph class.  It is very similar to Graph class with the addition of a couple of methods aimed at a graph of nodes that are directed.  Currently this class does not ensure that it is acyclic, but it is assumed that the user will not violate this principle.
    """
    
    def __init__(self, nodes):
        Graph.__init__(self, nodes)
        self.topological_sort()
    
    def topological_sort(self):
        # Orders nodes such that no node is before any of its parents.
        sorted = list()
        while len(nodes) > 0:
            for node in nodes:
                if Utilities.issuperset(sorted, node.parents):
                    sorted.append(node)
                    nodes.remove(node)
                    break
        return sorted 
    
    def undirect(self):
        for node in self.nodes:
            node.undirect()


class BayesNet(DAG):
    """  This is an actual Bayesian Network.  It is essentially a DAG, but it has several extra methods and fields that are used by associated inference and learning algorithms.
    """
    
    def __init__(self, nodes):
        DAG.__init__(self, nodes)
        self.numNodes = len(nodes)
                
    def children (self, i):
        return self.nodes[i].children

    def parents (self, i):
        return self.nodes[i].parents
    
    def nodeSize(self, i):
        return self.nodes[i].nodeSize
    
    def index_of(self, node):
        # This function is hides the actual implementation of self.nodes, keeping up an abstraction barrier
        return self.nodes.index(node)
    
    def counts(self):
        # Return an array of matrices that can be used as a way to build a set of counts
        # This is also breaking down the abstraction barrier by accessing CPT, 
        # should be investigated at a later date.
        return [copy.deepcopy(node.dist) for node in self.nodes]
    
    def add_counts(self, counts):
        # Update the internal CPTs with the given counts
        for node in self.nodes:
            count = counts[node.index]
            node.dist += count
            node.dist.normalize()
    
    def update_counts(self, counts, evidence):
        for node in self.nodes:
            count = counts[node.index]
            evIndex = node.evidence_index()
            values = evidence[evIndex]
            index = count.generateIndex(evIndex, range(count.nDims))
            count[index] += 1

            
class MoralGraph(Graph):
    """  A MoralGraph is an undirected graph that is built by connecting all of the parents of a directed graph and dropping the direction of the edges.
    """
    
    def __init__(self, DAG):
        Graph.__init__(self, DAG.nodes)
        #undirect the nodes
        for node in self.nodes:
            node.undirect()
        #connect all pairs of parents
        for node in self.nodes:
            parents = node.parents
            for i in range(len(parents)):
                for parent in parents[i:]:
                    self.connect_nodes(node.parents[i], parent)

class MoralDBNGraph(MoralGraph):
    """ This is not finished yet.  The plan is to use this class to create a MoralGraph for use in Dynamic Bayes Nets. The primary difference between doing JunctionTreeInference on a DBN from a static bayes net is that I have to ensure that the forward interface and the backward interface are both contained in a clique of the final join tree.  This can be ensured by making sure that all of the nodes in the two interfaces are connected.  For more details and a justification please see Kevin Murphy's dissertation.
    """
    
    def __init__(self, DBN):
        MoralGraph.__init__(DBN)
        fInterfaceNodes = self.selectForwardInterface()
        bInterfaceNodes = self.selectBackInterface()
        
        #make sure all nodes within the interface are connected
        for interface in [fInterfaceNodes, bInterfaceNodes]:
            #for each interface, connect all nodes within the interface
            for i in range(len(interface)):
                for node in interface[i+1:]:
                    self.connect_nodes(interface[i], node)
                    

class TriangleGraph(Graph):
    """ TriangleGraph is constructed from the MoralGraph.  It is the triangulated graph.  It is constructed by identifying clusters of nodes according to a given heuristic.  There are many heuristics that can be used, and in this implementation the heuristic is implemented in the ClusterBinaryHeap and can therefore be changed independent of this class.  The heap acts as a priority queue.  After the heap has been created, we remove nodes from the heap and use the information to create Cliques.  The Cliques are then added to the graph if they are not contained in a previous Clique.  TODO: Move addClique to this class from GraphUtilities.  Reimplement ClusterBinaryHeap as a built in python priority queue.
    """
    
    def __init__(self, moral):
        Graph.__init__(self, moral.nodes)
        heap = ClusterBinaryHeap()
        # Copy the graph so that we can destroy the copy as we insert it into heap.
        for i, node in enumerate(copy.deepcopy(moral.nodes)):
            node.index = i
            heap.insert(node)
        inducedCliques = []
        for (node, edges) in heap:
            realnode = self.nodes[node.index]
            for edge in edges:
                # We need to make sure we reference the nodes in the actual graph, 
                # not the copied ones that were inserted into the heap.
                node1 = self.nodes[node.neighbors[edge[0]].index]
                node2 = self.nodes[node.neighbors[edge[1]].index]
                self.connect_nodes(node1, node2)
            clique = Clique([realnode] + realnode.neighbors)
            # We only add clique to inducedCliques if is not contained in a previously added clique
            GraphUtilities.addClique(inducedCliques, clique) 
        self.cliques = inducedCliques
        

class JoinTree(Graph):
    """ JoinTree is the final graph that is constructed for JunctionTree Inference.  To create the JoinTree, we first create a forest of n JoinTrees where each tree consists of a single clique (n is the number of cliques).  Then we create a list of all distinct pairs.  Then we insert a sepset between each pair of cliques.  Then we loop n - 1 times.  At each iteration, we choose the next best sepset according to some heuristic.  If we the two cliques connected to the sepset are on different trees, we join them into one larger tree.    
    """
    
    #use constructor from Graph, will take either a single clique or a list of them
    def __init__(self, clique):
        if not isinstance(clique, types.ListType):
            clique = [clique]
        Graph.__init__(self, clique)
        self.initialized = False
        self.likelihoods = []
    
    def init_clique_potentials(self, variables):
        # We currently only handle one tree long forests.
        for v in variables:
            famV = v.parents + [v]
            for clique in self.nodes:
                if clique.contains(famV):
                    v.clique = clique
                    clique.init_potential(v)
                    break
        self.initialized = True
    
    def merge(self, sepset, tree):
        cliqueX = sepset.cliqueX
        cliqueY = sepset.cliqueY                
        cliqueX.add_neighbor(cliqueY)
        cliqueY.add_neighbor(cliqueX)
        cliqueX.add_sepset(sepset)
        cliqueY.add_sepset(sepset)
        for node in tree.nodes:
            self.add_node(node)
    
    def reinitialize(self, variables):
        for clique in self.nodes:
            clique.reinit_potential()
            # FIXME: the following optimizes each sepset twice, inefficient.
            for sepset in clique.sepsets:
                sepset.reinit_potential()
        self.init_clique_potentials(variables)
    
    def enter_evidence(self, evidence, nodes):
        mask = evidence != -1
        values = evidence[mask]
        nodeIndices = array(range(len( nodes )))[mask]
        for (nodeI, value) in zip(nodeIndices, values):
            node = nodes[nodeI]
            clique = node.clique
            axis = [clique.nodes.index(node)]
            # FIXME: This really should be a plain numarray object and 
            # then indexed with a slice object
            potentialMask = Potential(clique.nodes)
            potentialMask[:] = 0
            index = potentialMask.generateIndex(value, axis)
            potentialMask[index] = 1
            clique.potential[:] *= potentialMask[:]   
    