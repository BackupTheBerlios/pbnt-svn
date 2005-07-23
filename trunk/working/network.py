import 

class Network:
  
  def __init__(self, adjacencyMat):
    
    #an adjacency matrix that specifies the network structure.
    #if i,j = 1 then there is a directed arrow from i to j, in other words j is the child of i.
    self.madjacencyMat = adjacencyMat
    self.numberOfNodes = adjacencyMat.shape[0]
    
  def parents (self, node):
    
    #select the 
    parentColumn = take (self.madjacencyMat, (node,), axis=1)
    
    
    
    
    