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
                        famV = v.parents + [v]
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
                nodeIndices = array(range(len( nodes )))[mask]
                
                for (nodeI, value) in zip( nodeIndices, values ):
                        #perfect example of why attr CPT needs to be renamed
                        node = nodes[nodeI]
                        clique = node.clique
                        axis = [clique.nodes.index( node )]
                        axesToIter = [i for i in range(clique.CPT.nDims) if not i == axis]
                        potentialMask = DiscreteDistribution(zeros( array(clique.CPT.dims), type=Float32 ), node.nodeSize)
                        if len( axesToIter ) > 0:
                                dimsToIter = array(clique.CPT.dims)[axesToIter]
                                indices = generateArrayIndex( dimsToIter, axesToIter, [value], [axis] )
                                potentialMask.CPT.setValue( indices, 1 )
                        else:
                                potentialMask.CPT.setValue( array([value]), 1, axes=axis)
                        
                        clique.CPT.CPT *= potentialMask.CPT        
                        
                        
                        
                        
                        
                
                
                                
                        
                
                
        
        