

class PriorityQueue:
        
        def __init__( self ):
                self.queue = []
        
        def insert( self, node ):
                self.queue.append( node )
                self.queue.sort()
        
        def __iter__( self ):
                return self.queue
                