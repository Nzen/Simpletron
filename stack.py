
class Stack( object ) :
	
	def __init__( self ) :
		' why am I reimplementing this? I am this close to trashing this '
		self.stak = [ ]
		self.top = -1
	
	def pop( self ) :
		if Stack.empty( self ) :
			print "fail"
			exit( 1 )
		else :
			self.top -= 1
			return self.stak[ self.top + 1 ]
		
	def peek( self ) :
		" This is why, lists don't appear to offer peek "
		if Stack.empty( self ) :
			print "fail"
			exit( 1 )
		else :
			return self.stak[ self.top ]
		
	def notEmpty( self ) :
		return 0 <= self.top
		
	def empty( self ) :
		return 0 > self.top
	
	def push( self, val ) :
		self.top += 1
		self.stak.append( val )

	def printStack( self ) :
		# lord, python for loops.
		if Stack.notEmpty( self ) :
			for ind in range( 0, self.top ) :
				print "%s " % self.stak[ ind ],
			print
		else :
			print "Stack Empty"