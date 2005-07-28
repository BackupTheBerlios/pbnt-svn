from BayesNode import *

class Clique( BayesNode ):
        
        def __init__( self, nodes ):
                BayesNode.__init__( self, len( nodes ) )
                self.nodes = nodes
                self.neighbors = []
                self.sepsets = []
                self.initialized = False
                self.CPT = DiscreteDistribution( ones([node.ns for node in self.nodes]), self.nodes[o].ns )
                
        
        def addSepset( self, sepset ):
                self.sepsets.append( sepset )
                
        def initPotential( self, variable ):
                sequence = SequenceGenerator( variable.CPT.dims )
                cliqueAxes = [self.nodes.index(node) for node in variable.parents + [variable]]
                for seq in sequence:
                        self.CPT.setMultipleValues( seq, cliqueAxes, variable.CPT.getValue( seq ) )
        
                        