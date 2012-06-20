
class Ram( object ):
	
	maxAddr = 100 # Python's lists may be dynamic, but let's simulate real limits
	#max used # nevermind, if you want the size, ask for Ram.maxAddr or len( ramm.memory )
	
	def __init__( self ):
		self.memory = [ 0 ] * Ram.maxAddr
	
	def setAt( self, addr, val ):
		' I"m expecting the client (cpu) to handle addresses out of bounds '
		self.memory[ addr ] = val
	
	def getFrom( self, addr ):
		' I"m expecting the client to handle addresses out of bounds '
		return self.memory[ addr ]
		
	def exceedAddrBound( self, anAddr ):
		' is this address too big? '
		return anAddr < 0 or Ram.maxAddr < anAddr
	
	def coreDump( self, dumpSite ):	# vetted 11 12 7
		'prints memory (only) to a file because of some error'
		endl = 0
		for yy in range( 0, 10 ) : # should reflect memory size
			dumpSite.write( '\t' + str( yy ) )
		for nn in self.memory:
			if 0 == endl % 10 :
				dumpSite.write( '\n' + str( endl ) + '\t' ) # 00xx
			dumpSite.write( str( nn ).rjust( 4, '0' ) + '\t' ) # doesn't need to be \n\r
			endl += 1
			
	def loader( self, file ) :
		" I decided it is ram's responsibility to load itself "
		memNext = 0
		temp = 0
		try:
			hdSector = open( file, 'r' )
			for line in hdSector:
				if not line.startswith( "##" ) :
					if Ram.exceedAddrBound( self, memNext ) :
						continue
					else :
						Ram.setAt( self, memNext, int( line[ :-1 ] ) )
						memNext += 1
				else:
					break # so I can put comments below that line
					# I thought I'd cut it but testing the compiler is much easier with comments
				temp += 1
			hdSector.close( )
		except IOError:
			print "File to load not found, perhaps it's not here with me?"
			exit( 1 )
