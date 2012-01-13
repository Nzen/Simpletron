
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
			
	def loader( self, files ) :
		" I decided it is ram's responsibility to load itself "
		memNext = 0
		temp = 0
		try:
			for nn in files :
				hdSector = open( nn )
				for line in hdSector:
					if not line.startswith( "##" ) :
						if Ram.exceedAddrBound( self, memNext ) :
							continue
						else :
							Ram.setAt( self, memNext, int( line[ :-1 ] ) )
							memNext += 1
					else:
						break # so I can put comments below that line
						# I should consider cutting this aspect once I have a compiler
						# but still, then I can comment it afterward? Dude, do you
						# put comments in binaries? well, binaries are not for education.
					temp += 1
				hdSector.close( )
		except IOError:
			print "oh shit, file not found probably"
			# I'll have to figure out that part, but it has been tested in comp.py