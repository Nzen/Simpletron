
class TableEntry( object ) :
	
	def __init__( self ) :
		symbol = ""
		type = 0
		location = 0
		# values to be overwritten
		
	def setType( self, newType ) :
		TableEntry.type = newType
		
	def setSymbol( self, symbolToAdopt ) :
		TableEntry.symbol = symbolToAdopt
		
	def setLocation( self, newAddr ) :
		TableEntry.location = newAddr
		
	def getType( self ) :
		return TableEntry.type
		
	def getSymbol( self ) :
		return TableEntry.symbol
	
	# I think location is the only one I won't check after setting