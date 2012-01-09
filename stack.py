
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
		# they do, but you have to keep track of top then, don't you
		# which means TADA creating a stack class. STL ftw.
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
		' it turns out mixing these techniques incurs complexity '
		self.top += 1
		if len( self.stak ) == self.top :
			# then I have maxed the list size and pushing will overflow
			self.stak.append( val )
		else :
			# I am overwriting old values
			self.stak[ self.top ] = val

	def printStack( self ) :
		# lord, python For loops.
		if Stack.notEmpty( self ) :
			print "stack:\t",
			for ind in range( 0, self.top + 1 ) :
				print "%s " % self.stak[ ind ],
			print
		else :
			print "Stack Empty"