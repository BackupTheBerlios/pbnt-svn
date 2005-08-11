from numarray import *
import GraphUtilities

from ClusterBinaryHeap import *
from Clique import *

class Graph:
        #for now this class is designed for JoinTrees, eventually this will be abstracted and used as a global graphical class.
        
        #a graph can be thought of as a collection of nodes or a collection of edges, in this case we do both, will refine later.
        def __init__( self, nodes ):
                self.nodes = nodes
                
        def addNode( self, node ):
                if isinstance( node, types.ListType ):
                        for n in node:
                                self.nodes.append( n )
                else:
                        self.nodes.append( node )
                
        def memberOf( self, node ):
                return node in self.nodes


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


class MoralGraph(Graph):
        
        def __init__(self, DAG):
                Graph.__init__(self, DAG.nodes)
                
                #undirect the nodes
                for node in self.nodes:
                        node.undirect()
                
                #connect all pairs of parents
                for node in self.nodes:
                        parents = node.parents
                        for i in range(len(parents)):
                                for parent in parents[i:]:
                                        GraphUtilities.connectNodes(node.parents[i], parent)

class MoralDBNGraph(MoralGraph):
        
        def __init__(self, DBN):
                MoralGraph.__init__(DBN)
                #for the DBN case, we need to connect all of the nodes in the forward
                #and backward interfaces respectively.  This will insure that the Interfaces
                #end up in entailed within a clique.  See Kevin Murphy's Thesis section 3 the
                #Interface Algorithm for more details.
                fInterfaceNodes = self.selectForwardInterface()
                bInterfaceNodes = self.selectBackInterface()
                
                #make sure all nodes within the interface are connected
                for interface in [fInterfaceNodes, bInterfaceNodes]:
                        #for each interface, connect all nodes within the interface
                        for i in range(len(interface)):
                                for node in interface[i+1:]:
                                        GraphUtilities.connectNodes(interface[i], node)
                                        

class TriangleGraph(Graph):
        
        def __init__(self, moral):
                Graph.__init__(self, moral.nodes)
                heap = ClusterBinaryHeap()
                #copy the graph so that we can destroy the copy as we go
                for (node, i) in zip(copy.deepcopy(moral.nodes), range(len(moral.nodes))):
                        node.index = i
                        #have to copy so that when we destory neighbor lists it wont affect the actual graph
                        heap.insert(node)
                
                inducedCliques = []
                for (node, edges) in heap:
                        realnode = self.nodes[node.index]
                        for edge in edges:
                                #a little messy, but we want to reference the nodes in the actual graph, not the ones from the heap
                                #we destroyed the neighbor lists of the nodes in the heap
                                GraphUtilities.connectNodes(self.nodes[node.neighbors[edge[0]].index], self.nodes[node.neighbors[edge[1]].index])
                        
                        clique = Clique([realnode] + realnode.neighbors)
                        #use addCluster which only adds if it is not contained in a previously added cluster
                        GraphUtilities.addClique(inducedCliques, clique) 
                        
                
                self.cliques = inducedCliques

class JoinTree(Graph):
        
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
                cliqueX = sepset.cliqueX
                cliqueY = sepset.cliqueY                
                cliqueX.addNeighbor( cliqueY )
                cliqueY.addNeighbor( cliqueX )
                cliqueX.addSepset( sepset )
                cliqueY.addSepset( sepset )
                for node in tree.nodes:
                        self.addNode( node )
                #self.addNode( sepset.cliqueY )
        
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
                        #axesToIter = [i for i in range(clique.CPT.nDims) if not i == axis]
                        potentialMask = DiscreteDistribution(zeros( array(clique.CPT.dims), type=Float32 ), node.nodeSize)
                        potentialMask.setValue( value, 1, axes=axis )
                        #if len( axesToIter ) > 0:
                                #dimsToIter = array(clique.CPT.dims)[axesToIter]
                                #indices = generateArrayIndex( dimsToIter, axesToIter, [value], [axis] )
                                #potentialMask.CPT.setValue( indices, 1 )
                        #else:
                                #potentialMask.CPT.setValue( array([value]), 1, axes=axis)
                        
                        clique.CPT.CPT *= potentialMask.CPT        
        