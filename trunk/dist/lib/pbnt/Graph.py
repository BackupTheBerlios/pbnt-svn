from numarray import *
import GraphUtilities
from ClusterBinaryHeap import *
from Clique import *

class Graph:
    """ Graph is the parent of all other graph classes.  It defines a very basic undirected graph class.  It essentially is 
    just a list of nodes, and it is the nodes that maintain their own lists of parents and children.
    """
    
    def __init__(self, nodes):
        self.nodes = set(nodes)
        
    def add_node(self, node):
        # Check if it is a list of nodes or a single node (arrays are also type=ListType).
        if isinstance(node, types.ListType):
            for n in node:
                self.nodes.append(n)
        else:
            self.nodes.append(node)
        
    def member_of(self, node):
        return node in self.nodes
    
    def contains(self, nodes):
        assert(isinstance(nodes, set))
        return self.nodes.issuperset(nodes)

class DAG(Graph):
    """ Child of Graph class.  It is very similar to Graph class with the addition of a couple of methods aimed at a graph of
    nodes that are directed.  Currently this class does not ensure that it is acyclic, but it is assumed that the user
    will not violate this principle.
    """
    
    def __init__(self, nodes):
        self.nodes = self.topological_sort(nodes)
    
    def topological_sort(self, nodes):
        # Orders nodes such that no node is before any of its parents.
        noParents = []
        children = []
        for node in nodes:
            if len(node.parents) == 0:
                noParents.append(node)
            #not FINISHED 
    
    def undirect(self):
        for node in self.nodes:
            node.undirect()


class BayesNet( DAG ):
    
    def __init__(self, nodes):
        DAG.__init__( self, nodes )
        self.numNodes = len(nodes)
                
    def children (self, i):
        return self.nodes[i].children

    def parents (self, i):
        return self.nodes[i].parents
    
    def parentIndices( self, i ):
        indices = []
        for node in self.nodes[i].parents:
            indices.append(self.indexOf( node ))
        return array(indices)
    
    def numberOfNodes(self):
        return self.numNodes
    
    def ns(self, i):
        return self.nodes[i].nodeSize
    
    def CPTs( self, i ):
        return self.nodes[i].CPT
    
    def indexOf( self, node ):
        return self.nodes.index( node )
    
    def counts(self):
        return array([node.CPT.CPT.copy() for node in self.nodes])
    
    def addCounts(self, counts):
        for node in self.nodes:
            node.CPT.CPT += counts[node.index]
            node.CPT.normalise()

            
class MoralGraph(Graph):
    
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
                    GraphUtilities.connectNodes(node.parents[i], parent)

class MoralDBNGraph(MoralGraph):
    
    def __init__(self, DBN):
        MoralGraph.__init__(DBN)
        #for the DBN case, we need to connect all of the nodes in the forward
        #and backward interfaces respectively.  This will insure that the Interfaces
        #end up in entailed within a clique.  See Kevin Murphy's Thesis section 3 the
        #Interface Algorithm for more details.
        fInterfaceNodes = self.selectForwardInterface()
        bInterfaceNodes = self.selectBackInterface()
        
        #make sure all nodes within the interface are connected
        for interface in [fInterfaceNodes, bInterfaceNodes]:
            #for each interface, connect all nodes within the interface
            for i in range(len(interface)):
                for node in interface[i+1:]:
                    GraphUtilities.connectNodes(interface[i], node)
                    

class TriangleGraph(Graph):
    
    def __init__(self, moral):
        Graph.__init__(self, moral.nodes)
        heap = ClusterBinaryHeap()
        #copy the graph so that we can destroy the copy as we go
        for (node, i) in zip(copy.deepcopy(moral.nodes), range(len(moral.nodes))):
            node.index = i
            #have to copy so that when we destory neighbor lists it wont affect the actual graph
            heap.insert(node)
        
        inducedCliques = []
        for (node, edges) in heap:
            realnode = self.nodes[node.index]
            for edge in edges:
                #a little messy, but we want to reference the nodes in the actual graph, not the ones from the heap
                #we destroyed the neighbor lists of the nodes in the heap
                GraphUtilities.connectNodes(self.nodes[node.neighbors[edge[0]].index], self.nodes[node.neighbors[edge[1]].index])
            
            clique = Clique([realnode] + realnode.neighbors)
            #use addCluster which only adds if it is not contained in a previously added cluster
            GraphUtilities.addClique(inducedCliques, clique) 
            
        
        self.cliques = inducedCliques

class JoinTree(Graph):
    
    #use constructor from Graph, will take either a single clique or a list of them
    def __init__( self, clique ):
        if not isinstance( clique, types.ListType ):
            clique = [clique]
        
        Graph.__init__( self, clique )
        self.initialized = False
        self.likelihoods = []
    
    def initCliquePotentials( self, variables ):
        #if the join tree was created we are guaranteed to have a parent cluster
        #if there is no such cluster, we must be one tree in a forest and it must be in
        #another tree
        for v in variables:
            famV = v.parents + [v]
            for clique in self.nodes:
                if clique.contains( famV ):
                    v.clique = clique
                    clique.initPotential( v )
                    break
        self.initialized = True
    
    def merge( self, sepset, tree ):
        cliqueX = sepset.cliqueX
        cliqueY = sepset.cliqueY                
        cliqueX.addNeighbor( cliqueY )
        cliqueY.addNeighbor( cliqueX )
        cliqueX.addSepset( sepset )
        cliqueY.addSepset( sepset )
        for node in tree.nodes:
            self.addNode( node )
        #self.addNode( sepset.cliqueY )
    
    def re_initialize( self, variables ):
        for clique in self.nodes:
            clique.reinitPotential()
            #need to optimize the next part as is it does double the work it should
            for sepset in clique.sepsets:
                sepset.reinitPotential()
        self.initCliquePotentials( variables )
    
    def enter_evidence( self, evidence, nodes ):
        mask = evidence != -1
        values = evidence[mask]
        nodeIndices = array(range(len( nodes )))[mask]
        
        for (nodeI, value) in zip( nodeIndices, values ):
            #perfect example of why attr CPT needs to be renamed
            node = nodes[nodeI]
            clique = node.clique
            axis = [clique.nodes.index( node )]
            #axesToIter = [i for i in range(clique.CPT.nDims) if not i == axis]
            potentialMask = DiscreteDistribution(zeros( array(clique.CPT.dims), type=Float32 ), node.nodeSize)
            potentialMask.setValue( value, 1, axes=axis )
            #if len( axesToIter ) > 0:
                #dimsToIter = array(clique.CPT.dims)[axesToIter]
                #indices = generateArrayIndex( dimsToIter, axesToIter, [value], [axis] )
                #potentialMask.CPT.setValue( indices, 1 )
            #else:
                #potentialMask.CPT.setValue( array([value]), 1, axes=axis)
            
            clique.CPT.CPT *= potentialMask.CPT        
    