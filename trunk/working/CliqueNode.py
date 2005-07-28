from BayesNode import *

class CliqueNode( BayesNode ):
        
        def __init__( self, node ):
                self = node
                self.clique = -1
        