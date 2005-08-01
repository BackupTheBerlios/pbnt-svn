from BayesNode import *
from DiscreteDistribution import *
from SequenceGenerator import *
from GraphUtilities import *

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
                        if len( axesToIter ) > 0:
                                dimsToIter = array(self.CPT.dims)[axesToIter]
                                indices = generateArrayIndex( dimsToIter, axesToIter, seq, cliqueAxes )
                        else: 
                                indices = seq
                        self.CPT.setValue( indices, values )        
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
        
                        