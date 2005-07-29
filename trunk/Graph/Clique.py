from BayesNode import *
from CliqueNode import *
from DiscreteDistribution import *
from SequenceGenerator import *

class Clique( BayesNode ):
        
        def __init__( self, nodes ):
                #nodes = [CliqueNode( node ) for node in nodes]
                BayesNode.__init__( self, len( nodes ) )
                self.nodes = nodes
                self.neighbors = []
                self.sepsets = []
                self.CPT = DiscreteDistribution( ones([node.nodeSize for node in self.nodes], type=Float), self.nodes[0].nodeSize )
                
        
        def addSepset( self, sepset ):
                self.sepsets.append( sepset )
                
        def initPotential( self, variable ):
                sequence = SequenceGenerator( variable.CPT.dims )
                cliqueAxes = [self.nodes.index(node) for node in variable.parents + [variable]]
                for seq in sequence:
                        cliqueValues = self.CPT.getValue( seq, cliqueAxes )
                        variableValues = variable.CPT.getValue( seq )
                        values = cliqueValues * variableValues
                        self.CPT.setMultipleValues( seq, cliqueAxes, values )
        
        def reinitPotential( self ):
                self.CPT = DiscreteDistribution( ones([node.nodeSize for node in self.nodes]), self.nodes[0].nodeSize )
        
        def contains( self, nodes ):
                isIn = True
                for node in nodes:
                        if not node in self.nodes:
                                isIn = False
                                break
                return isIn
        
                        