from DAG import *
import utilities

class MoralGraph( Graph ):
        
        def __init__( self, DAG ):
                Graph.__init__( self, DAG.nodes[:] )
                
                #undirect the nodes
                for node in self.nodes:
                        node.undirect()
                
                #connect all pairs of parents
                for node in self.nodes:
                        parents = node.parents
                        for i in range(len( parents )):
                                for parent in parents[i:]:
                                        utilities.connectNodes( node.parents[i], parent )
        