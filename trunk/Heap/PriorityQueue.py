

class PriorityQueue:
        
        def __init__( self ):
                self.queue = []
                self.i = -1
        
        def insert( self, node ):
                self.queue.append( node )
                self.queue.sort()
        
        def __iter__( self ):
                self.i = -1
                return self
        
        def next( self ):
                if self.i == len( self.queue ) - 1:
                        raise StopIteration
                self.i += 1
                return self.queue[self.i]
        
        def hasNext( self ):
                return len( self.queue ) > 0
        
        def init( self ):
                self.i = -1