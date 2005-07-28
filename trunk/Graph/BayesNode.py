from DirectedNode import *

class BayesNode( DirectedNode ):
        
        #this is a node for a Bayesian Network, which is a directed node with some extra fields
        def __init__( self, nodeSize ):
                DirectedNode.__init__( self )
                self.nodeSize = nodeSize
        
        def setCPT( self, CPT ):
                self.CPT = CPT