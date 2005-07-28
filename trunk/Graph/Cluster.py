from Node import *

class ClusterNode( Node ):
        #These are clusters in the Join Tree sense
        def __init__( self, neighbors, sepsets, potential ):
                Node.__init__( self, neighbors )
                self.potential = potential
                self.sepsets = sepsets
        
        
                