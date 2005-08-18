import Utilities
from numarray import *
from DiscreteDistribution import *

class Node:
    """ A Node is the basic element of a graph.  In its most basic form a graph is just a list of nodes.  A Node is a really just a list of neighbors.  
    """
    def __init__(self, id, index=-1, name="anonymous"):
        # This defines a list of edges to other nodes in the graph.
        self.neighbors = []
        self.visited = False
        self.id = id
        # The index of this node within the list of nodes in the overall graph.
        self.index = index
        # Optional name, most usefull for debugging purposes.
        self.name = name
    
    def __lt__(self, other):
        # Defines a < operator for this class, which allows for easily sorting a list of nodes.
        return self.index < other.index
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, right):
        return self.id == right.id
            
    def add_neighbor(self, node):
        """ Make node a neighbor if it is not alreadly.  This is a hack, we should be allowing self to be a neighbor of self in some graphs.  This should be enforced at the level of a graph, because that is where the type of the graph would disallow it.
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
    """ This is the child class of Node.  Instead of mainting a list of neighbors, it maintains a list of parents and children.  Of course since it is the child of Node, it does technically have a list of neighbors (though it should remain empty).
    """
    def __init__(self, id, index=-1, name="anonymous"):
        Node.__init__(self, id, index, name)
        self.parents = []
        self.children = []
        # The following is used commonly to index into the evidence.
        self.parentIndex = []
    
    def add_parent(self, parent):
        # Same as add_neighbor, but for parents of the node.
        if not (parent in self.parents or self == parent):
            self.parents.append(parent)
            self.parentIndex.append(parent.index)
    
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
        """ This drops the direction of self's edges.  This doesn't exactly destroy it since self still maintains lists of parents and children.  We could think of this as allowing us to treat self as both directed and undirected simply allowing it to be casted as one at one moment and the other at another moment.
        """
        self.neighbors = self.parents + self.children

class BayesNode(DirectedNode):
    """ BayesNode is a child class of DirectedNode.  Essentially it is a DirectedNode with some added fields that make it more appropriate for a Bayesian Network, such as a field for a distribution and arrays of indices. The arrays are indices of its parents and children; that is the index of its neighbor within the overall bayes net.
    """
    #this is a node for a Bayesian Network, which is a directed node with some extra fields
    def __init__(self, id, numValues, index=-1, name="anonymous"):
        DirectedNode.__init__(self, id, index, name)
        self.numValues = numValues
        # value is the value that this node currently holds.  -1 is currently the "Blank" value, this feels dangerous.
        self.value = -1
        self.clique = -1
        
    def evidence_index(self):
        return self.parentIndex + [self.index]
        
    def set_dist(self, dist):
        self.dist = dist
    
    def size(self):
        return self.t
    
    def __len__(self):
        return self.dist.size


class Clique(Node):
    """ Clique inherits from Node.  Clique's are clusters which act as a single node within a JoinTree. They are equivalent in JoinTrees to BayesNodes' in Bayesian Networks.  The main difference is that they have "potentials" instead of distributions.  Potentials are in effect the same as a conditional distribution, but unlike conditional distribtions, there isn't as clear a sense that the distribution is over one node and conditioned on a number of others.
    """    
    
    def __init__(self, nodes):
        # Make the name of self the concatenation of the names of the input nodes.
        name = ''
        for node in nodes:
            name += node.name
        Node.__init__(self, name)
        self.nodes = nodes
        # Nodes must be ordered in the same relative order that they are in the actual network, so that they are in topo order.
        self.nodes.sort()
        # Between every Clique node is a sepset, so this should be as long as 
        self.sepsets = []
        # A Potential is like a conditional distribution, but the probabilities 
        # are not explicitly conditioned on other probabilities.
        self.potential = Potential(self.nodes)
    
    def add_neighbor(self, sepset, node):
        Node.add_neighbor(node)
        self.sepsets.append(sepset)
                
    def init_potential(self, node):
        """ We can either iterate through all of the dimensions of node, or all of the dimensions of self.potential that are not related to node.  Which ever is fewer will be faster. 
        """
        parentIndices = [self.nodes.index(node) for node in variable.parents + [variable]]
        nNodeDims = len(node.parents) + 1
        if nNodeDims < (self.potential.nDims - nNodeDims):
            # Iterate over the node's dimensions.
            # axes is a list of the index of each of the nodes relative to the clique, 
            # we will use this to know how to permute the the indices into the node, 
            # so that they are equivalent to the clique's own potential.
            axes = parentIndices
            # An iterator that iterates through all possible indices of node.
            sequence = SequenceGenerator(node.dist.dims)
            for seq in sequence:
                cliqueValues = self.dist.get_value(seq, axes)
                nodeValues = variable.dist.get_value(seq)
                values = cliqueValues * nodeValues
                self.potential.set_value(seq, values, axes)    
        else:
            mask = zeros([self.potential.nDims], type=Bool)
            mask[parentIndices] = 0
            # axes is a list of the axes that are not related to node.
            axes = arange(self.potential.nDims)[mask]
            axesDims = self.potential.dims[axes]
            sequence = SequenceGenerator(axesDims)
            for seq in sequence:
                cliqueValues = self.dist.get_value(seq, axes)
                nodeValues = node.dist.CPT
                values = cliqueValues * nodeValues
                self.potential.set_value(seq, values, axes)
                
    def reinit_potential( self ):
        self.potential = Potential(self.nodes)
    
    def contains(self, nodes):
        # Checks if all of nodes is contained in self.nodes
        isIn = True
        for node in nodes:
            if not node in self.nodes:
                isIn = False
                break
        return isIn
 

class Sepset( Node ):
    """ Sepsets sit between Cliques in a join tree.  They represent the intersection of the variables in the two member Cliques.  They facilitate passing messages between the two cliques.
    """
    
    def __init__(self, cliqueX, cliqueY):
        Node.__init__(self)
        # Clique that is connected to one side of self
        self.cliqueX = cliqueX
        # Clique that is connected to the other side of self.
        self.cliqueY = cliqueY
        # The nodes that are in self
        self.nodes = utilities.intersect(cliqueX.nodes, cliqueY.nodes)
        # Make sure that they are in topo order
        self.nodes.sort()
        # The mass of self (the number of nodes it relates to.
        self.mass = len(self.nodes)
        # The cost, used for breaking ties between mass.  The cost is equal to the 
        # product of the node sizes of the nodes in cliqueX + cliqueY. 
        costX = product(array([node.dist.size() for node in cliqueX.nodes]))
        costY = product(array([node.dist.size() for node in cliqueY.nodes]))
        self.cost = costX + costY
        self.neighbors = [cliqueX, cliqueY]
        self.potential = Potential(self.nodes)
        self.cliqueXAxes = array([cliqueX.nodes.index(node) for node in self.nodes])
        self.cliqueYAxes = array([cliqueY.nodes.index(node) for node in self.nodes])
        
    
    def clique_axes(self, clique):
        # Return the clique axes that match the input clique.
        if clique == self.cliqueX:
            return self.cliqueXAxes
        else:
            return self.cliqueYAxes
    
    
    def __lt__(self, other):
        # This test is used to order nodes when deciding which sepset has highest priority.
        if self.mass > other.mass:
            return True
        if self.mass == other.mass and self.cost < other.cost:
            return True
        
        return False
    
    def reinit_potential(self):
        self.potential = Potential(self.nodes)