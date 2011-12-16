
class Ram( object ):
	
	maxAddr = 100 # Python's lists may be dynamic, but let's simulate real limits
	#max used # nevermind, if you want the size, ask for Ram.maxAddr or len( ramm.memory )
	
	def __init__( self ):
		self.memory = [ 0 ] * Ram.maxAddr
	
	def setAt( self, addr, val ):
		' I"m expecting the client to handle addresses out of bounds '
		self.memory[ addr ] = val
	
	def getFrom( self, addr ):
		' I"m expecting the client to handle addresses out of bounds '
		return self.memory[ addr ]
		
	def exceedAddrBound( self, anAddr ):
		' is this address too big? '
		if anAddr < 0 :
			return True
		elif Ram.maxAddr < anAddr :
			return True
		else:
			return False
	
	def coreDump( self, dumpSite ):	# vetted 11 12 7
		'prints memory (only) to a file because of some error'
		endl = 0
		for yy in range( 0, 10 ) :
			dumpSite.write( '\t' + str( yy ) )
		for nn in self.memory:
			if 0 == endl % 10 :
				dumpSite.write( '\n' + str( endl ) + '\t' ) # 00xx
			dumpSite.write( str( nn ).rjust( 4, '0' ) + '\t' ) # doesn't need to be \n\r
			endl += 1