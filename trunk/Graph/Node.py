

class Node:
        #essentially a basic element of a graph, at some point create a child class that has a distribution
        
        def __init__( self ):
                #neighbors are actually connected by an edge, in a DAG neighbors = parents + children
                self.neighbors = []
                self.visited = False
                #this is a little messy, but need a back reference to the graph
                self.index = -1
                       
        def addNeighbor( self, node ):
                #this is a hack to check if node == self, fix later
                if not (node in self.neighbors or self == node):
                        self.neighbors.append( node )
        
        def removeNeighbor( self, node ):
                self.neighbors.remove( node )
        
        def isNeighbor( self, node ):
                return node in self.neighbors
        