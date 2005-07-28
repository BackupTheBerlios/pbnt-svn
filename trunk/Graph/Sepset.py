from Node import *
from SequenceGenerator import *
import utilities

class Sepset( Node ):
        
        def __init__( self, cliqueX, cliqueY ):
                Node.__init__( self )
                self.cliqueX = cliqueX
                self.cliqueY = cliqueY
                self.nodes = utilities.intersect( cliqueX.nodes, cliqueY.nodes )
                
                self.neighbors = [cliqueX, cliqueY]
                dims = [x.ns for x in self.nodes]
                self.potential = DiscreteDistribution( ones(dims), self.nodes[0].ns )
                
                self.axis = range( self.potential.nDims )
                self.mu = [seq for seq in SequenceGenerator( dims )]
                self.cliqueXAxes = [cliqueX.nodes.index( node ) for node in self.nodes]
                self.cliqueYAxes = [cliqueY.nodes.index( node ) for node in self.nodes]
                
        
        def cliqueAxes( self, clique ):
                if clique == self.cliqueX:
                        return self.cliqueXAxes
                else:
                        return self.cliqueYAxes
                
                
                
                
                
        