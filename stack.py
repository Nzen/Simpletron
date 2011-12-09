
class Stack( object ) :
	
	def __init__( size ) :
		self.stak = list( size ) # maybe? I saw this used but couldn't find the doc
		self.top = -1
	
	def pop( ) :
		self.top -= 1
		return self.stak[ top + 1 ]
		
	def peek( ) :
		return self.stak[ top ]
		
	def notEmpty( ) :
		return 0 <= self.top
	
	def push( val ) :
		self.top += 1
		self.stak[ top ] = val