import GraphUtilities
from numarray import *

class InducedCluster:
        
        def __init__( self, node ):
                self.node = node
                self.edges = GraphUtilities.missingEdges( self.node )
                self.nEdges = len( self.edges )
                self.weight = self.computeWeight()
        
        
        def __lt__( self, other ):
                #less than means that it is better (pick it first)
                if self.nEdges < other.nEdges:
                        return True
                if self.nEdges == other.nEdges and self.weight < other.weight:
                        return True
                
                return False
        
        def recompute( self ):
                self.edges = GraphUtilities.missingEdges( self.node )
                self.nEdges = len( self.edges )
                self.weight = self.computeWeight()
        
        def computeWeight( self ):
                return product(array( [node.nodeSize for node in self.node.neighbors] + [self.node.nodeSize] ))