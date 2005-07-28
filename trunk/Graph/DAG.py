from Graph import *


#right now same as graph, but will use topo which is difference
class DAG(Graph):
        
        #a directed graph
        #ASSUMPTION: nodes in topo order
        def __init__( self, nodes ):
                self.nodes = nodes
                #self.nodes = topologicalSort( nodes )
                self.numNodes = len( nodes )
        
        def topologicalSort( self, nodes ):
                #puts nodes in topo order, parents before children
                noParents = []
                children = []
                for node in nodes:
                        if len( node.parents ) == 0:
                                noParents.append( node )
                 #not FINISHED 
        
        def undirect( self ):
                for node in self.nodes:
                        node.undirect()
        
                                