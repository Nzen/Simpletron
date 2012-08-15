
# Fuck, now I have to build something analagous.

class struct( object ) :
	def __init__( self ) :
		self.symbol = ""
	#def __init__( self, name ) :
	#	self.symbol = name

class handleBob( object ) :
	def __init__( self ) :
		self.many = [ struct() for i in range( 5 ) ]
		## this pattern is called a list comprehension
		# it avoids reference multiplication
		self.farthest = -1
	
	def show( self ) :
		print "  Here's what's inside:"
		ind = 0
		lim = self.farthest
		while ind <= lim :
			print self.many[ ind ].symbol
			ind += 1
	
	def warp( self, name ) :
		self.farthest += 1
		ind = self.farthest
		
		self.many[ ind ].symbol = name

names = [ "banana", "Doge", "Ferrari", "halibut", "xake" ]
analog = handleBob( )
for word in names :
	analog.show( )
	analog.warp( word )
'''
class handles( object ) :
	def __init__( self ) :
		self.many = [ struct() ] * 5
		self.farthest = -1
	
	def show( self ) :
		print "  Here's what's inside:"
		ind = 0
		lim = self.farthest
		while ind <= lim :
			print self.many[ ind ].symbol
			ind += 1
	
	def warp( self, name ) :
		self.farthest += 1
		ind = self.farthest
		
		self.many[ ind ].symbol = name
		
class handlerThing( object ) :
	def __init__( self ) :
		self.many = [ None ]
		self.farthest = -1
	
	def show( self ) :
		print "  Here's what's inside:"
		ind = 0
		lim = self.farthest
		while ind <= lim :
			if self.many[ ind ] is not None :
				print self.many[ ind ].symbol
			ind += 1
	
	def warp( self, name ) :
		self.farthest += 1
		self.many.append( struct( name ) )
'''
'''
	RESULT: sullen vindication
 >> handles
  Here's what's inside:
  Here's what's inside:
banana
  Here's what's inside:
Doge
Doge
  Here's what's inside:
Ferrari
Ferrari
Ferrari
  Here's what's inside:
halibut
halibut
halibut
halibut

>> handlerThing
  Here's what's inside:
  Here's what's inside:
  Here's what's inside:
banana
  Here's what's inside:
banana
Doge
  Here's what's inside:
banana
Doge
Ferrari

>> handleBob ; vindication for them

  Here's what's inside:
  Here's what's inside:
banana
  Here's what's inside:
banana
Doge
  Here's what's inside:
banana
Doge
Ferrari
  Here's what's inside:
banana
Doge
Ferrari
halibut

http://comscigate.com/ib/cs/dossier/year2003/BobCao/index.htm
'''