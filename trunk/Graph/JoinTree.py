from Graph import *

class JoinTree( Graph ):
        
        #use constructor from Graph
        def __init__( self, clique ):
                Graph.__init__( self, [clique] )
        
        def initCliquePotentials( self, variables ):
                #if the join tree was created we are guaranteed to have a parent cluster
                #if there is no such cluster, we must be one tree in a forest and it must be in
                #another tree
                for v in variables:
                        famV = [v] + v.parents
                        for clique in self.nodes:
                                if clique.contains( famV ):
                                        clique.initPotential( v )
                                        break
        
        def merge( self, sepset, tree ):
                clique = sepset.cliqueX
                clique.addNeighbor( sepset.cliqueY )
                clique.addSepset( sepset )
                self.addNode( sepset.cliqueY )
                                
                        
                
                
        
        