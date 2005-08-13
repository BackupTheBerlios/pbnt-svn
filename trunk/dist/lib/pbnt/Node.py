from SequenceGenerator import *
import utilities
from numarray import *
from DiscreteDistribution import *

class Node:
    #essentially a basic element of a graph, at some point create a child class that has a distribution
    
    def __init__( self, index=-1, name="anonymous" ):
        #neighbors are actually connected by an edge, in a DAG neighbors = parents + children
        self.neighbors = []
        self.visited = False
        #this is a little messy, but need a back reference to the graph
        self.index = index
        self.name = name
    
    def __lt__( self, other ):
        return self.index < other.index
            
    def addNeighbor( self, node ):
        #this is a hack to check if node == self, fix later
        if not (node in self.neighbors or self == node):
            self.neighbors.append( node )
    
    def removeNeighbor( self, node ):
        self.neighbors.remove( node )
    
    def isNeighbor( self, node ):
        return node in self.neighbors

class DirectedNode( Node ):
    
    def __init__( self, index=-1, name="anonymous" ):
        Node.__init__( self, index, name )
        self.parents = []
        self.children = []
    
    def addParent( self, parent ):
        self.parents.append( parent )
    
    def addChild( self, child ):
        self.children.append( child )
    
    def removeParent( self, parent ):
        self.parents.remove( parent )
        
    def removeChild( self, child ):
        self.children.remove( child )
    
    def undirect( self ):
        self.neighbors = self.neighbors + self.parents + self.children

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