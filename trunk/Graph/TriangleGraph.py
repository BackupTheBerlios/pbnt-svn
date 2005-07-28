from Graph import *
import GraphUtilities

class TriangleGraph( Graph ):
        
        def __init__( self, moral ):
                Graph.__init__( self, moral.nodes )
                heap = PriorityQueue( )
                for node in self.nodes:
                        heap.insert( node )
                
                inducedCliques = []
                for (node, edges) in heap:
                        for edge in edges:
                                GraphUtilities.connectNodes( node.neighbors[edge[0]], node.neighbors[edge[1]] )
                        
                        clique = Clique( [node] + node.neighbors )
                        #use addCluster which only adds if it is not contained in a previously added cluster
                        GraphUtilities.addClique( inducedCliques, clique ) 
                        
                
                self.cliques = inducedCliques
        
                        