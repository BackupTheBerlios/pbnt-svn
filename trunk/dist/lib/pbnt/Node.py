from SequenceGenerator import *
import utilities
from numarray import *
from DiscreteDistribution import *

class Node:
    """ A Node is the basic element of a graph.  In its most basic form a graph is just a list of 
    Nodes.  A Node is a really just a list of neighbors.  
    """
    def __init__(self, index=-1, name="anonymous"):
        # This defines a list of edges to other nodes in the graph.
        self.neighbors = []
        self.visited = False
        # The index of this node within the list of nodes in the overall graph.
        self.index = index
        # Optional name, most usefull for debugging purposes.
        self.name = name
    
    def __lt__(self, other):
        # Defines a < operator for this class, which allows for easily sorting a list of nodes.
        return self.index < other.index
            
    def add_neighbor(self, node):
        """ Make node a neighbor if it is not alreadly.  This is a hack, we should be allowing 
        self to be a neighbor of self in some graphs.  This should be enforced at the level of a 
        graph, because that is where the type of the graph would disallow it.
        """
        if not (node in self.neighbors or self == node):
            self.neighbors.append(node)
    
    def remove_neighbor(self, node):
        # Remove the node from the list of neighbors, effectively deleting that edge from
        # the graph.
        self.neighbors.remove(node)
    
    def is_neighbor(self, node):
        # Check if node is a member of neighbors.
        return node in self.neighbors

class DirectedNode(Node):
    """ This is the child class of Node.  Instead of mainting a list of neighbors, it maintains
    a list of parents and children.  Of course since it is the child of Node, it does technically
    have a list of neighbors (though it should remain empty).
    """
    def __init__(self, index=-1, name="anonymous"):
        Node.__init__(self, index, name)
        self.parents = []
        self.children = []
    
    def add_parent(self, parent):
        # Same as add_neighbor, but for parents of the node.
        if not (parent in self.parents or self == parent):
            self.parents.append(parent)
    
    def add_child(self, child):
        # Same as add_parent but for children.
        if not (child in self.children or self == child):
            self.children.append(child)
    
    def remove_parent(self, parent):
        # Same as remove_neighbor, but for parents.
        self.parents.remove(parent)
        
    def remove_child(self, child):
        # Same as remove_parent
        self.children.remove(child)
    
    def undirect( self ):
        """ This drops the direction of self's edges.  This doesn't exactly destroy it since 
        self still maintains lists of parents and children.  We could think of this as allowing
        us to treat self as both directed and undirected simply allowing it to be casted as one
        at one moment and the other at another moment.
        """
        self.neighbors = self.parents + self.children

class BayesNode( DirectedNode ):
    
    #this is a node for a Bayesian Network, which is a directed node with some extra fields
    def __init__( self, nodeSize, index=-1, name="anonymous" ):
        DirectedNode.__init__( self, index, name )
        self.nodeSize = nodeSize
        #this is really something that should be in a child class named CliqueNode, but don't know how
        #to coerce it to change type in place on the fly
        self.clique = -1
        self.evidence = -1
        self.parentIndex = array( [node.name for node in self.parents] )
        self.childIndex = array( [node.name for node in self.children] )
        
        
    def setCPT( self, CPT ):
        self.CPT = CPT

#So far Clique is only used in JTree
class Clique( BayesNode ):
    
    def __init__( self, nodes ):
        #nodes = [CliqueNode( node ) for node in nodes]
        BayesNode.__init__( self, len( nodes ) )
        self.nodes = nodes
        self.nodes.sort()
        self.neighbors = []
        self.sepsets = []
        self.CPT = DiscreteDistribution(ones([node.nodeSize for node in self.nodes], type=Float32), self.nodes[0].nodeSize )
        
    
    def addSepset( self, sepset ):
        self.sepsets.append( sepset )
        
    def initPotential( self, variable ):
        cliqueAxes = [self.nodes.index(node) for node in variable.parents + [variable]]
        sequence = SequenceGenerator( variable.CPT.dims )
        axesToIter = [axis for axis in range(self.CPT.nDims) if not axis in cliqueAxes]
        #this could be greatly optimized, first generateArrayIndex could be called only once and then replace
        #the constant values with new ones for each seq
        #Also: will be fastest if sequence is over the smallest number of dimensions, either
        #the variables or the non-variable dimensions
        for seq in sequence:
            cliqueValues = self.CPT.getValue( seq, cliqueAxes )
            variableValues = variable.CPT.getValue( seq )
            values = cliqueValues * variableValues
            self.CPT.setValue( seq, values, cliqueAxes )
            #if len( axesToIter ) > 0:
                #dimsToIter = array(self.CPT.dims)[axesToIter]
                #indices = generateArrayIndex( dimsToIter, axesToIter, seq, cliqueAxes )
            #else: 
                #indices = seq
            #self.CPT.setValue( indices, values )        
            #if len( axesToIter ) > 0:
            
            #else:
                #self.CPT.setValue( seq, values, axes=cliqueAxes)
            
    
    def reinitPotential( self ):
        self.CPT = DiscreteDistribution(ones([node.nodeSize for node in self.nodes], type=Float32), self.nodes[0].nodeSize )
    
    def contains( self, nodes ):
        isIn = True
        for node in nodes:
            if not node in self.nodes:
                isIn = False
                break
        return isIn

#Cluster is generally only used in Junction Tree
class ClusterNode( Node ):
    #These are clusters in the Join Tree sense
    def __init__( self, neighbors, sepsets, potential ):
        Node.__init__( self, neighbors )
        self.potential = potential
        self.sepsets = sepsets
    
    
#Also only used in JTree
class Sepset( Node ):
    
    def __init__( self, cliqueX, cliqueY ):
        Node.__init__( self )
        self.cliqueX = cliqueX
        self.cliqueY = cliqueY
        self.nodes = utilities.intersect( cliqueX.nodes, cliqueY.nodes )
        self.nodes.sort()
        self.mass = len( self.nodes )
        self.cost = product(array( [node.nodeSize for node in cliqueX.nodes] )) + product(array( [node.nodeSize for node in cliqueY.nodes] ))
        
        self.neighbors = [cliqueX, cliqueY]
        self.dims = [x.nodeSize for x in self.nodes]
        self.indexWeights = array([product(self.dims[i+1:]) for i in range(len( self.dims ))])
        self.potential = DiscreteDistribution( ones(self.dims, type=Float32), self.nodes[0].nodeSize )
        
        self.axis = range( self.potential.nDims )
        self.mu = SequenceGenerator( self.dims )
        self.cliqueXAxes = [cliqueX.nodes.index( node ) for node in self.nodes]
        self.cliqueYAxes = [cliqueY.nodes.index( node ) for node in self.nodes]
        
    
    def clique_axes(self, clique):
        if clique == self.cliqueX:
            return self.cliqueXAxes
        else:
            return self.cliqueYAxes
    
    
    def __lt__( self, other ):
        #less than essentially means better than
        if self.mass > other.mass:
            return True
        if self.mass == other.mass and self.cost < other.cost:
            return True
        
        return False
    
    def reinitPotential( self ):
        self.potential = DiscreteDistribution( ones(self.dims, type=Float32), self.nodes[0].nodeSize )