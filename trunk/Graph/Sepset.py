from Node import *
from SequenceGenerator import *
import utilities
from numarray import *
from DiscreteDistribution import *

class Sepset( Node ):
        
        def __init__( self, cliqueX, cliqueY ):
                Node.__init__( self )
                self.cliqueX = cliqueX
                self.cliqueY = cliqueY
                self.nodes = utilities.intersect( cliqueX.nodes, cliqueY.nodes )
                self.mass = len( self.nodes )
                self.cost = product(array( [node.nodeSize for node in cliqueX.nodes] )) + product(array( [node.nodeSize for node in cliqueY.nodes] ))
                
                self.neighbors = [cliqueX, cliqueY]
                self.dims = [x.nodeSize for x in self.nodes]
                self.potential = DiscreteDistribution( ones(self.dims, type=Float32), self.nodes[0].nodeSize )
                
                self.axis = range( self.potential.nDims )
                self.mu = SequenceGenerator( self.dims )
                self.cliqueXAxes = [cliqueX.nodes.index( node ) for node in self.nodes]
                self.cliqueYAxes = [cliqueY.nodes.index( node ) for node in self.nodes]
                
        
        def cliqueAxes( self, clique ):
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
                        
                
                
                
                
        