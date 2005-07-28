from numarray import *
from DAG import *

class BayesNet( DAG ):
	
	def __init__(self, nodes):
		DAG.__init__( self, nodes )
				
	def children (self, i):
		return self.nodes[i].children

	def parents (self, i):
		return self.nodes[i].parents
	def parentIndices( self, i ):
		indices = []
		for node in self.nodes[i].parents:
			indices.append(self.indexOf( node ))
		return array(indices)
	
	def numberOfNodes(self):
		return self.numNodes
	
	def ns(self, i):
		return self.nodes[i].nodeSize
	def CPTs( self, i ):
		return self.nodes[i].CPT
	
	def indexOf( self, node ):
		return self.nodes.index( node )

		

		
