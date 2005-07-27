from numarray import *

class Graph:
        #for now this class is designed for JoinTrees, eventually this will be abstracted and used as a global graphical class.
        
        #a graph can be thought of as a collection of nodes or a collection of edges, in this case we do both, will refine later.
        def __init__( self, nodes ):
                self.nodes = nodes
        