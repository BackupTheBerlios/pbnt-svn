from Node import *


class DirectedNode( Node ):
        
        def __init__( self, index=-1, name="anonymous" ):
                Node.__init__( self, index, name )
                self.parents = []
                self.children = []
        
        def addParent( self, parent ):
                self.parents.append( parent )
        
        def addChild( self, child ):
                self.children.append( child )
        
        def removeParent( self, parent ):
                self.parents.remove( parent )
                
        def removeChild( self, child ):
                self.children.remove( child )
        
        def undirect( self ):
                self.neighbors = self.neighbors + self.parents + self.children
        
        
                
        