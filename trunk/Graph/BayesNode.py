from DirectedNode import *

class BayesNode( DirectedNode ):
        
        #this is a node for a Bayesian Network, which is a directed node with some extra fields
        def __init__( self, nodeSize, index=-1, name="anonymous" ):
                DirectedNode.__init__( self, index, name )
                self.nodeSize = nodeSize
                #this is really something that should be in a child class named CliqueNode, but don't know how
                #to coerce it to change type in place on the fly
                self.clique = -1
                self.evidence = -1
        
        def setCPT( self, CPT ):
                self.CPT = CPT