

class Node:
        #essentially a basic element of a graph, at some point create a child class that has a distribution
        
        def __init__( self ):
                #neighbors are actually connected by an edge, in a DAG neighbors = parents + children
                self.neighbors = []
                self.visited = False
                       
        def addNeighbor( self, node ):
                if not node in self.neighbors:
                        self.neighbors.append( node )
        
        def removeNeighbor( self, node ):
                self.neighbors.remove( node )
                
                
        