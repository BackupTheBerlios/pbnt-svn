from Graph import *
from DiscreteDistribution import *

class JoinTree( Graph ):
        
        #use constructor from Graph, will take either a single clique or a list of them
        def __init__( self, clique ):
                if not isinstance( clique, types.ListType ):
                        clique = [clique]
                
                Graph.__init__( self, clique )
                self.initialized = False
                self.likelihoods = []
        
        def initCliquePotentials( self, variables ):
                #if the join tree was created we are guaranteed to have a parent cluster
                #if there is no such cluster, we must be one tree in a forest and it must be in
                #another tree
                for v in variables:
                        famV = [v] + v.parents
                        for clique in self.nodes:
                                if clique.contains( famV ):
                                        v.clique = clique
                                        clique.initPotential( v )
                                        break
                self.initialized = True
        
        def merge( self, sepset, tree ):
                clique = sepset.cliqueX
                clique.addNeighbor( sepset.cliqueY )
                clique.addSepset( sepset )
                self.addNode( sepset.cliqueY )
        
        def reInitialize( self, variables ):
                for clique in self.nodes:
                        clique.reinitPotential()
                        #need to optimize the next part as is it does double the work it should
                        for sepset in clique.sepsets:
                                sepset.reinitPotential()
                self.initCliquePotentials( variables )
        
        def enterEvidence( self, evidence, nodes ):
                mask = evidence != -1
                values = evidence[mask]
                nodeIndices = array( nodes )[mask]
                
                for (nodeI, value) in zip( nodeIndices, values ):
                        #perfect example of why attr CPT needs to be renamed
                        node = nodes[nodeI]
                        clique = node.clique
                        axis = [clique.nodes.index( node )]
                        potentialMask = DiscreteDistribution(zeros( [clique.CPT.dims], type=Float ), node.nodeSize)
                        potentialMask.setMultipleValues( array([value]), axis, 1 )
                        clique.CPT.CPT *= potentialMask        
                        
                        
                        
                        
                
                
                                
                        
                
                
        
        